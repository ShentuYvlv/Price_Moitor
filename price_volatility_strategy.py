import time
from datetime import datetime
import os
import ccxt
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import (
    Strategy, get_socks5_proxy, get_perpetual_symbols, 
    save_perpetual_symbols, load_perpetual_symbols, 
    check_price_task, get_candle_id, find_previous_volatility
)

class PriceVolatilityStrategy(Strategy):
    """价格异动策略"""
    def __init__(self):
        super().__init__("价格异动策略")
        self.volatile_pairs = []  # 保存已发出警报的交易对
        self.last_candle_id = None  # 上一次K线的ID
        self.volatility_threshold = 5  # 波动阈值（5%）
        self.max_workers = 50  # 线程池大小
    
    def initialize(self):
        """初始化策略"""
        print(f'初始化{self.name}...')
        # 初始化币安交易所
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'timeout': 30000,
            'proxies': get_socks5_proxy(),
            'options': {
                'defaultType': 'future',  # 设置为合约模式
                'adjustForTimeDifference': True,
                'recvWindow': 60000
            },
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        })
        
        # 首次获取并保存永续合约交易对
        current_symbols = get_perpetual_symbols(self.exchange)
        save_perpetual_symbols(current_symbols)
        
        # 创建结果目录
        os.makedirs("results", exist_ok=True)
        
        self.is_running = True
        print(f'{self.name}初始化完成')
    
    def execute(self):
        """执行策略"""
        try:
            while self.is_running:
                start_time = time.time()
                
                # 检查新的交易对
                new_symbols = get_perpetual_symbols(self.exchange)
                symbols = load_perpetual_symbols()
                added_symbols = set(new_symbols) - set(symbols)
                
                if added_symbols:
                    print("\n发现新的永续合约交易对:")
                    for symbol in sorted(added_symbols):
                        print(f"新交易对: {symbol}")
                    save_perpetual_symbols(new_symbols)
                    symbols = new_symbols
                else:
                    print("没有新的交易对 开始更新价格数据")

                # 批量获取所有交易对的K线数据
                print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始检查价格波动...")
                total_symbols = len(symbols)
                print(f"总共需要检查 {total_symbols} 个交易对")
                
                # 使用线程池并发检查
                current_volatile_pairs = []  # 当前检测中波动较大的交易对
                completed = 0
                all_results = []  # 存储所有交易对的检查结果
                current_candle_id = None  # 当前K线ID
                
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {executor.submit(check_price_task, self.exchange, symbol): symbol for symbol in symbols}
                    
                    for future in as_completed(futures):
                        completed += 1
                        if completed % 10 == 0 or completed == total_symbols:
                            progress = (completed / total_symbols) * 100
                            time_elapsed = time.time() - start_time
                            print(f"\r进度: {completed}/{total_symbols} ({progress:.1f}%) - 已用时: {time_elapsed:.1f}秒", end="")
                        
                        result = future.result()
                        if result:
                            result['check_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            all_results.append(result)
                            
                            if current_candle_id is None and 'timestamp' in result:
                                current_candle_id = get_candle_id(result['timestamp'])
                                
                                if self.last_candle_id is not None and current_candle_id != self.last_candle_id:
                                    print(f"\n\n检测到新的K线周期(ID从{self.last_candle_id}变为{current_candle_id})，清空之前的波动记录")
                                    self.volatile_pairs.clear()
                            
                            if abs(result['up_vol']) > self.volatility_threshold or abs(result['down_vol']) > self.volatility_threshold:
                                prev_record = find_previous_volatility(result['symbol'], self.volatile_pairs)
                                need_alert = False
                                
                                if prev_record is None:
                                    need_alert = True
                                    self.volatile_pairs.append(result)
                                else:
                                    if (abs(result['up_vol']) > abs(prev_record['up_vol']) + self.volatility_threshold or
                                        abs(result['down_vol']) > abs(prev_record['down_vol']) + self.volatility_threshold):
                                        need_alert = True
                                        for i, pair in enumerate(self.volatile_pairs):
                                            if pair['symbol'] == result['symbol']:
                                                self.volatile_pairs[i] = result
                                                break
                                
                                if need_alert:
                                    current_volatile_pairs.append(result)
                
                print()  # 换行
                
                # 处理发现的大波动交易对
                if current_volatile_pairs:
                    print("\n发现大波动交易对:")
                    current_volatile_pairs.sort(key=lambda x: max(abs(x['up_vol']), abs(x['down_vol'])), reverse=True)
                    
                    for pair in current_volatile_pairs:
                        prev_record = find_previous_volatility(pair['symbol'], self.volatile_pairs)
                        if prev_record and prev_record != pair:
                            up_change = pair['up_vol'] - prev_record['up_vol']
                            down_change = pair['down_vol'] - prev_record['down_vol']
                            print(f"{pair['symbol']}: 上涨{pair['up_vol']:.2f}%(变化:{up_change:+.2f}%) 下跌{pair['down_vol']:.2f}%(变化:{down_change:+.2f}%)")
                        else:
                            print(f"{pair['symbol']}: 上涨{pair['up_vol']:.2f}% 下跌{pair['down_vol']:.2f}%")
                
                # 更新K线ID
                if current_candle_id is not None:
                    self.last_candle_id = current_candle_id
                
                # 计算用时
                end_time = time.time()
                print(f"\n本轮检查用时: {end_time - start_time:.2f}秒")
                
                time.sleep(10)
                
        except Exception as e:
            print(f'{self.name}执行出错:', str(e))
            print(f"错误类型: {type(e).__name__}") 