import time
from datetime import datetime
import os
import ccxt
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import (
    Strategy, get_socks5_proxy, get_perpetual_symbols, 
    save_perpetual_symbols, load_perpetual_symbols, 
    check_price_task, get_candle_id, find_previous_volatility,
    get_bybit_perpetual_symbols, get_okx_perpetual_symbols,
    send_email, fetch_market_data
)
import traceback
import random
from collections import defaultdict

# 添加常量定义
OKX_RATE_LIMIT = 20  # OKX每秒请求限制
OKX_RATE_LIMIT_RESET = 1.0  # OKX限制重置时间(秒)
MAX_RETRY_ATTEMPTS = 3  # 最大重试次数

class PriceVolatilityStrategy(Strategy):
    """价格异动策略"""
    def __init__(self, selected_exchanges=None, main_exchange=None):
        super().__init__("价格异动策略")
        self.volatile_pairs = []  # 保存已发出警报的交易对
        self.last_candle_id = None  # 上一次K线的ID
        self.volatility_threshold = 3.0  # 默认波动阈值（2%），应当被前端传入的值覆盖
        self.max_workers = 20  # 默认线程池大小，降低以避免过多并发请求
        self.selected_exchanges = selected_exchanges if selected_exchanges else ["binance","okx","bybit"]  # 默认使用币安、OKX和Bybit
        self.main_exchange = main_exchange  # 主交易所，优先处理
        self.exchanges = {}  # 交易所实例字典
        self.pairs_sources = {}  # 交易对与其数据源交易所的映射
        self.okx_symbols = []  # OKX交易所的交易对
        self.all_symbols = []  # 所有交易所的交易对并集
        
        # 新增支持的参数（这些参数应当被前端传入的值覆盖）
        self.time_period = 300  # 默认1分钟 (60秒)
        self.monitor_direction = "both"  # both, up, down
        self.refresh_interval = 10  # 默认10秒刷新一次
        self.results_queue = None  # 结果队列，用于向API传递数据
        self.top_volatile_pairs = []  # 储存波动最大的交易对
        self.is_running = False
        
        # 添加API请求限制相关属性
        self.exchange_request_counts = defaultdict(int)  # 各交易所请求计数
        self.exchange_last_reset = defaultdict(float)  # 各交易所上次重置时间
        self.failed_pairs = []  # 获取失败的交易对
        
        # 调试标志 - 用于跟踪参数设置
        self.debug_initialized = False
    
    def initialize(self):
        """初始化策略"""
        print(f'初始化{self.name}...')
        
        # 确保已选交易所不为空，否则使用默认值
        if not self.selected_exchanges:
            self.selected_exchanges = ["binance", "okx", "bybit"]
            print(f"未指定交易所，使用默认值: {self.selected_exchanges}")
        
        # 设置主交易所，如果未设置或不在已选交易所中，使用第一个已选交易所
        if not self.main_exchange or self.main_exchange not in self.selected_exchanges:
            self.main_exchange = self.selected_exchanges[0]
            print(f"主交易所未设置或不在已选列表中，自动设置为: {self.main_exchange}")
        
        print(f"已选交易所: {self.selected_exchanges}")
        print(f"主交易所: {self.main_exchange}")
        
        # 初始化选择的交易所
        for exchange_id in self.selected_exchanges:
            print(f"初始化交易所: {exchange_id}")
            try:
                if exchange_id == "binance":
                    self.exchanges["binance"] = ccxt.binance({
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
                    # 确保预加载市场数据
                    self.exchanges["binance"].load_markets()
                elif exchange_id == "okx":
                    self.exchanges["okx"] = ccxt.okx({
                        'enableRateLimit': True,
                        'timeout': 30000,
                        'proxies': get_socks5_proxy(),
                        'options': {
                            'defaultType': 'swap',  # OKX设置为永续合约模式
                            'adjustForTimeDifference': True,
                        },
                        'headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                    })
                    # 确保预加载市场数据
                    self.exchanges["okx"].load_markets()
                elif exchange_id == "bybit":
                    self.exchanges["bybit"] = ccxt.bybit({
                        'enableRateLimit': True,
                        'timeout': 30000,
                        'proxies': get_socks5_proxy(),
                        'options': {
                            'defaultType': 'swap',  # Bybit设置为永续合约模式
                            'adjustForTimeDifference': True,
                        },
                        'headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                    })
                    # 确保预加载市场数据
                    self.exchanges["bybit"].load_markets()
            except Exception as e:
                print(f"连接{exchange_id}交易所失败: {str(e)}")
                print(f"尝试不使用代理连接{exchange_id}交易所...")
                try:
                    if exchange_id == "binance":
                        self.exchanges["binance"] = ccxt.binance({
                            'enableRateLimit': True,
                            'timeout': 30000,
                            'options': {
                                'defaultType': 'future',  # 设置为合约模式
                                'adjustForTimeDifference': True,
                                'recvWindow': 60000
                            },
                            'headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            }
                        })
                        # 确保预加载市场数据
                        self.exchanges["binance"].load_markets()
                    elif exchange_id == "okx":
                        self.exchanges["okx"] = ccxt.okx({
                            'enableRateLimit': True,
                            'timeout': 30000,
                            'options': {
                                'defaultType': 'swap',  # OKX设置为永续合约模式
                                'adjustForTimeDifference': True,
                            },
                            'headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            }
                        })
                        # 确保预加载市场数据
                        self.exchanges["okx"].load_markets()
                    elif exchange_id == "bybit":
                        self.exchanges["bybit"] = ccxt.bybit({
                            'enableRateLimit': True,
                            'timeout': 30000,
                            'options': {
                                'defaultType': 'swap',  # Bybit设置为永续合约模式
                                'adjustForTimeDifference': True,
                            },
                            'headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            }
                        })
                        # 确保预加载市场数据
                        self.exchanges["bybit"].load_markets()
                    print(f"不使用代理成功连接到{exchange_id}交易所")
                except Exception as e2:
                    print(f"连接{exchange_id}交易所失败(无代理): {str(e2)}")
                    continue
        
        if not self.exchanges:
            print("错误: 未选择任何交易所或所有交易所连接失败")
            return
            
        # 获取每个交易所的交易对
        exchange_symbols = {}
        for exchange_id, exchange in self.exchanges.items():
            print(f"获取{exchange_id}交易所的永续合约交易对...")
            if exchange_id == "binance":
                exchange_symbols[exchange_id] = get_perpetual_symbols(exchange)
            elif exchange_id == "okx":
                exchange_symbols[exchange_id] = get_okx_perpetual_symbols(exchange)
                self.okx_symbols = exchange_symbols[exchange_id]  # 保存OKX的交易对列表
            elif exchange_id == "bybit":
                exchange_symbols[exchange_id] = get_bybit_perpetual_symbols(exchange)
                
            print(f"{exchange_id}交易所共有{len(exchange_symbols[exchange_id])}个永续合约交易对")
        
        # 处理交易对并集和交易所来源关系
        self.process_symbols(exchange_symbols)
            
        # 首次获取并保存永续合约交易对
        save_perpetual_symbols(self.all_symbols)
        
        # 创建结果目录
        os.makedirs("results", exist_ok=True)
        
        self.is_running = True
        print(f'{self.name}初始化完成，监控{len(self.all_symbols)}个交易对')
        print(f'监控时间周期: {self.time_period}秒, 波动阈值: {self.volatility_threshold}%, 监控方向: {self.monitor_direction}, 刷新间隔: {self.refresh_interval}秒')
    
    def process_symbols(self, exchange_symbols):
        """处理多个交易所的交易对，确定并集和数据源"""
        # 确定所有交易对的并集
        all_symbols = set()
        for symbols in exchange_symbols.values():
            all_symbols.update(symbols)
        
        self.all_symbols = list(all_symbols)
        print(f"合并后共有{len(self.all_symbols)}个独特的永续合约交易对")
        
        # 确定每个交易对的数据源交易所
        for symbol in self.all_symbols:
            # 首先检查是否在主交易所中存在
            if self.main_exchange and self.main_exchange in exchange_symbols and symbol in exchange_symbols[self.main_exchange]:
                self.pairs_sources[symbol] = self.main_exchange
            # 如果没有主交易所或交易对不在主交易所中，检查是否在OKX中存在
            elif symbol in self.okx_symbols and "okx" in exchange_symbols:
                self.pairs_sources[symbol] = "okx"
            else:
                # 否则，使用提供此交易对的第一个交易所
                for exchange_id, symbols in exchange_symbols.items():
                    if symbol in symbols:
                        self.pairs_sources[symbol] = exchange_id
                        break
        
        # 打印交易对来源统计
        source_stats = {}
        for source in self.pairs_sources.values():
            source_stats[source] = source_stats.get(source, 0) + 1
        
        print("交易对数据来源统计:")
        for source, count in source_stats.items():
            print(f"  {source}: {count}个交易对")

    def check_price_for_pair(self, symbol):
        """检查单个交易对的价格变动"""
        source = self.pairs_sources.get(symbol)
        if not source or source not in self.exchanges:
            return None
            
        exchange = self.exchanges[source]
        
        # 添加频率限制检查和等待逻辑
        if source == "okx":
            self._respect_rate_limit(source)
            
        # 根据时间周期调整检查逻辑
        try:
            # 获取基本价格数据
            result = check_price_task(exchange, symbol)

            if result:
                # 处理不同的时间周期
                time_period_map = {
                    60: 60,     # 1分钟
                    300: 300,   # 5分钟
                    900: 900,   # 15分钟
                    1800: 1800, # 30分钟
                    3600: 3600  # 1小时
                }

                # 确定使用哪个时间周期
                period = time_period_map.get(self.time_period, 60)

                # 在结果中添加时间周期信息，以便后续处理
                result['time_period'] = self.time_period
                # 添加数据源标记
                result['source'] = source

            return result
        except Exception as e:
            error_str = str(e)
            print(f"检查{symbol}价格变动时出错: {source} {error_str}")
            
            # 如果是OKX的频率限制错误，添加到失败列表
            if source == "okx" and "Too Many Requests" in error_str:
                self.failed_pairs.append({"symbol": symbol, "source": source, "error": error_str})
                # 遇到限流时强制等待一段时间
                time.sleep(0.5 + random.random() * 0.5)  # 随机等待0.5-1秒
            return None
        
    # 添加API速率限制方法
    def _respect_rate_limit(self, exchange_id):
        """
        遵守交易所API的速率限制
        """
        current_time = time.time()
        
        # 检查是否需要重置计数器
        if current_time - self.exchange_last_reset.get(exchange_id, 0) >= OKX_RATE_LIMIT_RESET:
            self.exchange_request_counts[exchange_id] = 0
            self.exchange_last_reset[exchange_id] = current_time
            
        # OKX专用限流处理
        if exchange_id == "okx":
            if self.exchange_request_counts[exchange_id] >= OKX_RATE_LIMIT:
                # 计算需要等待的时间
                elapsed = current_time - self.exchange_last_reset[exchange_id]
                if elapsed < OKX_RATE_LIMIT_RESET:
                    sleep_time = OKX_RATE_LIMIT_RESET - elapsed + 0.1 + (random.random() * 0.2)
                    # print(f"OKX API限流，等待{sleep_time:.2f}秒...")
                    time.sleep(sleep_time)
                    # 重置计数器
                    self.exchange_request_counts[exchange_id] = 0
                    self.exchange_last_reset[exchange_id] = time.time()
            
        # 增加请求计数
        self.exchange_request_counts[exchange_id] += 1
        
    def fetch_pair_details(self, symbol, source):
        """获取交易对的详细信息（价格、资金费率、市值、持仓）"""
        try:
            if source not in self.exchanges:
                return None
                
            exchange = self.exchanges[source]
            
            # 根据交易所类型设置正确的市场类型
            if source == "binance":
                exchange.options['defaultType'] = 'future'
            elif source in ["okx", "bybit"]:
                exchange.options['defaultType'] = 'swap'
                
            # 使用fetch_market_data获取详细信息
            details = fetch_market_data(exchange, symbol)
            
            # 添加数据源标记
            details['source'] = source
            
            return details
        except Exception as e:
            print(f"获取{symbol}详细信息时出错: {str(e)}")
            return None
            
    def format_details_message(self, details):
        """格式化交易对详细信息为可读字符串"""
        if not details:
            return "无法获取详细信息"
            
        lines = []
        
        # 基本价格和来源信息
        source = details.get('source', '未知')
        current_price = details.get('current_price')
        previous_price = details.get('previous_price')
        
        # 价格变化
        price_change = ""
        if current_price and previous_price:
            change_percent = ((current_price - previous_price) / previous_price) * 100
            price_change = f"价格变化: {change_percent:+.2f}%"
        
        # 添加基本价格信息
        if current_price:
            lines.append(f"当前价格: {current_price}")
        if price_change:
            lines.append(price_change)
            
        # 添加资金费率信息
        funding_rate = details.get('funding_rate')
        if funding_rate is not None:
            lines.append(f"资金费率: {funding_rate:.4f}%")
            
        # 添加持仓量信息
        open_interest = details.get('open_interest')
        open_interest_amount = details.get('open_interest_amount')
        
        if open_interest:
            # 格式化持仓量，使用K, M, B等后缀
            if open_interest > 1_000_000_000:
                formatted_oi = f"{open_interest/1_000_000_000:.2f}B"
            elif open_interest > 1_000_000:
                formatted_oi = f"{open_interest/1_000_000:.2f}M"
            elif open_interest > 1_000:
                formatted_oi = f"{open_interest/1_000:.2f}K"
            else:
                formatted_oi = f"{open_interest:.2f}"
                
            lines.append(f"持仓量: {formatted_oi}")
            
        if open_interest_amount:
            # 格式化市值，使用K, M, B等后缀
            if open_interest_amount > 1_000_000_000:
                formatted = f"{open_interest_amount/1_000_000_000:.2f}B"
            elif open_interest_amount > 1_000_000:
                formatted = f"{open_interest_amount/1_000_000:.2f}M"
            elif open_interest_amount > 1_000:
                formatted = f"{open_interest_amount/1_000:.2f}K"
            else:
                formatted = f"{open_interest_amount:.2f}"
                
            lines.append(f"持仓市值: {formatted} USDT")
            
        # 组合所有信息
        return f"[{source}] " + " | ".join(lines)

    def should_monitor_direction(self, up_vol, down_vol):
        """根据监控方向配置确定是否应该监控该波动"""
        # 首先检查波动值是否超过阈值
        if abs(up_vol) < self.volatility_threshold and abs(down_vol) < self.volatility_threshold:
            return False
            
        # 然后根据监控方向进行筛选
        if self.monitor_direction == "both":
            return True
        elif self.monitor_direction == "up" and up_vol >= self.volatility_threshold:
            return True
        elif self.monitor_direction == "down" and down_vol <= -self.volatility_threshold:
            return True
        return False
    
    def execute(self):
        """执行策略"""
        try:
            while self.is_running:
                start_time = time.time()
                
                # 检查新的交易对
                new_symbols = set()
                for exchange_id, exchange in self.exchanges.items():
                    # 只处理用户选择的交易所
                    if exchange_id not in self.selected_exchanges:
                        continue
                        
                    if exchange_id == "binance":
                        # 确保币安设置为future模式并加载市场
                        exchange.options['defaultType'] = 'future'
                        exchange.load_markets()
                        binance_symbols = get_perpetual_symbols(exchange)
                        new_symbols.update(binance_symbols)
                    elif exchange_id == "okx":
                        # OKX需要设置为swap模式
                        exchange.options['defaultType'] = 'swap'
                        exchange.load_markets()
                        okx_symbols = get_okx_perpetual_symbols(exchange)
                        new_symbols.update(okx_symbols)
                    elif exchange_id == "bybit":
                        # Bybit需要设置为swap模式
                        exchange.options['defaultType'] = 'swap'
                        exchange.load_markets()
                        bybit_symbols = get_bybit_perpetual_symbols(exchange)
                        new_symbols.update(bybit_symbols)
                
                new_symbols = list(new_symbols)
                
                # 检查已有的交易对列表
                symbols = load_perpetual_symbols()
                added_symbols = set(new_symbols) - set(symbols)
                
                if added_symbols:
                    print("\n发现新的永续合约交易对:")
                    for symbol in sorted(added_symbols):
                        # 确定新交易对的数据源
                        source = None
                        # 首先检查主交易所
                        if self.main_exchange in self.exchanges:
                            exchange = self.exchanges[self.main_exchange]
                            if self.main_exchange == "binance":
                                exchange.options['defaultType'] = 'future'
                                exchange.load_markets()
                                binance_symbols = get_perpetual_symbols(exchange)
                                if symbol in binance_symbols:
                                    source = self.main_exchange
                            elif self.main_exchange == "okx":
                                exchange.options['defaultType'] = 'swap'
                                exchange.load_markets()
                                okx_symbols = get_okx_perpetual_symbols(exchange)
                                if symbol in okx_symbols:
                                    source = self.main_exchange
                            elif self.main_exchange == "bybit":
                                exchange.options['defaultType'] = 'swap'
                                exchange.load_markets()
                                bybit_symbols = get_bybit_perpetual_symbols(exchange)
                                if symbol in bybit_symbols:
                                    source = self.main_exchange
                        
                        # 如果主交易所中不存在，则检查其他所选交易所
                        if source is None:
                            for exchange_id, exchange in self.exchanges.items():
                                if exchange_id == self.main_exchange or exchange_id not in self.selected_exchanges:
                                    continue  # 已经检查过主交易所或不在所选交易所中

                                if exchange_id == "binance":
                                    # 确保币安设置为future模式并加载市场
                                    exchange.options['defaultType'] = 'future'
                                    exchange.load_markets()
                                    binance_symbols = get_perpetual_symbols(exchange)
                                    if symbol in binance_symbols:
                                        source = exchange_id
                                        break
                                elif exchange_id == "okx":
                                    # 确保OKX设置为swap模式并加载市场
                                    exchange.options['defaultType'] = 'swap'
                                    exchange.load_markets()
                                    okx_symbols = get_okx_perpetual_symbols(exchange)
                                    if symbol in okx_symbols:
                                        source = exchange_id
                                        break
                                elif exchange_id == "bybit":
                                    # 确保Bybit设置为swap模式并加载市场
                                    exchange.options['defaultType'] = 'swap'
                                    exchange.load_markets()
                                    bybit_symbols = get_bybit_perpetual_symbols(exchange)
                                    if symbol in bybit_symbols:
                                        source = exchange_id
                                        break
                        
                        self.pairs_sources[symbol] = source
                        print(f"新交易对: {symbol} (来源: {source})")
                    
                    save_perpetual_symbols(new_symbols)
                    symbols = new_symbols
                else:
                    print("没有新的交易对 开始更新价格数据")

                # 批量获取所有交易对的K线数据
                time_period_name = {
                    60: "1分钟",
                    300: "5分钟",
                    900: "15分钟",
                    1800: "30分钟",
                    3600: "1小时"
                }.get(self.time_period, f"{self.time_period}秒")
                
                print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始检查{time_period_name}内价格波动...")
                total_symbols = len(symbols)
                print(f"总共需要检查 {total_symbols} 个交易对")
                
                # 初始化失败交易对列表
                self.failed_pairs = []
                
                # 按交易所分组处理交易对，避免同时请求同一交易所过多
                exchange_symbols = {}
                for symbol in symbols:
                    source = self.pairs_sources.get(symbol)
                    if source and source in self.selected_exchanges:
                        if source not in exchange_symbols:
                            exchange_symbols[source] = []
                        exchange_symbols[source].append(symbol)
                
                # 使用线程池并发检查
                current_volatile_pairs = []  # 当前检测中波动较大的交易对
                all_results = []  # 存储所有交易对的检查结果
                current_candle_id = None  # 当前K线ID
                
                # 优先处理主交易所的交易对
                completed = 0
                total_processed = 0
                
                # 如果设置了主交易所，先处理主交易所的交易对
                if self.main_exchange and self.main_exchange in exchange_symbols:
                    main_exchange_symbols = exchange_symbols[self.main_exchange]
                    print(f"\n首先处理主交易所({self.main_exchange})的 {len(main_exchange_symbols)} 个交易对...")
                
                    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                        futures = {executor.submit(self.check_price_for_pair, symbol): symbol for symbol in main_exchange_symbols}

                        for future in as_completed(futures):
                            completed += 1
                            total_processed += 1
                            if completed % 10 == 0 or completed == len(main_exchange_symbols):
                                progress = (total_processed / total_symbols) * 100
                                time_elapsed = time.time() - start_time
                                print(f"\r进度: {total_processed}/{total_symbols} ({progress:.1f}%) - 已用时: {time_elapsed:.1f}秒", end="")

                            result = future.result()
                            if result:
                                result['check_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                all_results.append(result)

                                if current_candle_id is None and 'timestamp' in result:
                                    current_candle_id = get_candle_id(result['timestamp'])

                                    if self.last_candle_id is not None and current_candle_id != self.last_candle_id:
                                        print(f"\n\n检测到新的K线周期(ID从{self.last_candle_id}变为{current_candle_id})，清空之前的波动记录")
                                        self.volatile_pairs.clear()

                                # 检查波动是否符合阈值和方向要求
                                if self.should_monitor_direction(result['up_vol'], result['down_vol']):
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
                    
                    # 删除主交易所，因为已经处理过了
                    del exchange_symbols[self.main_exchange]
                
                # 处理非OKX且非主交易所的交易对
                non_okx_symbols = []
                for ex_id, ex_symbols in exchange_symbols.items():
                    if ex_id != "okx" and ex_id != self.main_exchange and ex_id in self.selected_exchanges:
                        non_okx_symbols.extend(ex_symbols)
                
                # 重置计数器
                completed = 0
                
                # 处理非OKX交易所交易对
                if non_okx_symbols:
                    print(f"\n处理其他非OKX交易所的 {len(non_okx_symbols)} 个交易对...")
                    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                        futures = {executor.submit(self.check_price_for_pair, symbol): symbol for symbol in non_okx_symbols}
                        
                        for future in as_completed(futures):
                            completed += 1
                            total_processed += 1
                            if completed % 10 == 0 or completed == len(non_okx_symbols):
                                progress = (total_processed / total_symbols) * 100
                                time_elapsed = time.time() - start_time
                                print(f"\r进度: {total_processed}/{total_symbols} ({progress:.1f}%) - 已用时: {time_elapsed:.1f}秒", end="")
                            
                            result = future.result()
                            if result:
                                result['check_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                all_results.append(result)
                                
                                if current_candle_id is None and 'timestamp' in result:
                                    current_candle_id = get_candle_id(result['timestamp'])
                                    
                                    if self.last_candle_id is not None and current_candle_id != self.last_candle_id:
                                        print(f"\n\n检测到新的K线周期(ID从{self.last_candle_id}变为{current_candle_id})，清空之前的波动记录")
                                        self.volatile_pairs.clear()
                                
                                # 检查波动是否符合阈值和方向要求
                                if self.should_monitor_direction(result['up_vol'], result['down_vol']):
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
                
                # 处理OKX交易所交易对 - 使用较小的线程池并添加延迟
                if "okx" in exchange_symbols and exchange_symbols["okx"] and "okx" in self.selected_exchanges:
                    okx_symbols = exchange_symbols["okx"]
                    completed = 0
                    smaller_max_workers = min(10, self.max_workers)  # 限制OKX并发请求
                    
                    print(f"\n处理OKX交易所的 {len(okx_symbols)} 个交易对...")
                    # 对OKX交易对进行随机排序，避免集中请求同一批交易对
                    random.shuffle(okx_symbols)
                    
                    with ThreadPoolExecutor(max_workers=smaller_max_workers) as executor:
                        futures = {}
                        # 分批提交，减少并发
                        batch_size = 5
                        for i in range(0, len(okx_symbols), batch_size):
                            batch = okx_symbols[i:i+batch_size]
                            for symbol in batch:
                                futures[executor.submit(self.check_price_for_pair, symbol)] = symbol
                            # 每批之间添加短暂延迟
                            time.sleep(0.2)
                        
                        for future in as_completed(futures):
                            completed += 1
                            total_processed += 1
                            if completed % 5 == 0 or completed == len(okx_symbols):
                                progress = (total_processed / total_symbols) * 100
                                time_elapsed = time.time() - start_time
                                print(f"\r进度: {total_processed}/{total_symbols} ({progress:.1f}%) - 已用时: {time_elapsed:.1f}秒", end="")
                            
                            result = future.result()
                            if result:
                                result['check_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                all_results.append(result)
                                
                                if current_candle_id is None and 'timestamp' in result:
                                    current_candle_id = get_candle_id(result['timestamp'])

                                # 检查波动是否符合阈值和方向要求
                                if self.should_monitor_direction(result['up_vol'], result['down_vol']):
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
                
                # 重试失败的交易对
                if self.failed_pairs:
                    retry_count = min(len(self.failed_pairs), 50)  # 限制重试数量
                    print(f"\n开始重试 {retry_count} 个失败的交易对...")
                    retried_results = self._retry_failed_pairs(self.failed_pairs[:retry_count])
                    
                    # 合并结果
                    if retried_results:
                        all_results.extend(retried_results)
                        
                        # 检查是否有需要添加到波动交易对的
                        for result in retried_results:
                            if self.should_monitor_direction(result['up_vol'], result['down_vol']):
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
                
                # 处理发现的大波动交易对
                top_volatile_pairs = []
                
                # 输出处理结果
                if current_volatile_pairs:
                    print("\n发现大波动交易对:")
                    # 按波动幅度排序，取绝对值最大的
                    current_volatile_pairs.sort(key=lambda x: max(abs(x['up_vol']), abs(x['down_vol'])), reverse=True)
                    
                    # 准备邮件内容
                    email_content = "发现大波动交易对:\n\n"
                    console_output = [] # 用于控制台输出的信息
                    
                    # 获取更多详细信息 - 只处理真正需要提醒的交易对
                    for pair in current_volatile_pairs:
                        symbol = pair['symbol']
                        source = pair.get('source', '未知')
                        prev_record = find_previous_volatility(symbol, self.volatile_pairs)
                        
                        # 基础价格波动信息
                        if prev_record and prev_record != pair:
                            up_change = pair['up_vol'] - prev_record['up_vol']
                            down_change = pair['down_vol'] - prev_record['down_vol']
                            base_info = f"{symbol} [{source}]: 上涨{pair['up_vol']:.2f}%(变化:{up_change:+.2f}%) 下跌{pair['down_vol']:.2f}%(变化:{down_change:+.2f}%)"
                        else:
                            base_info = f"{symbol} [{source}]: 上涨{pair['up_vol']:.2f}% 下跌{pair['down_vol']:.2f}%"
                            
                        # 输出基本价格波动信息
                        print(base_info)
                        
                        # 获取详细信息
                        print(f"  正在获取 {symbol} 的详细信息...")
                        details = self.fetch_pair_details(symbol, source)
                        details_info = self.format_details_message(details)
                        
                        # 输出详细信息
                        print(f"  {details_info}")
                        
                        # 为邮件内容准备信息
                        console_output.append(f"{base_info}\n  {details_info}")
                        email_content += f"{base_info}\n{details_info}\n\n"
                    
                        # 同时保存到top_volatile_pairs用于API返回
                        if details:
                            top_volatile_pairs.append({
                                'symbol': symbol,
                                'source': source,
                                'price': details.get('current_price', 0),
                                'up_vol': pair['up_vol'],
                                'down_vol': pair['down_vol'],
                                'funding_rate': details.get('funding_rate', 0),
                                'open_interest': details.get('open_interest', 0),
                                'open_interest_amount': details.get('open_interest_amount', 0),
                                'check_time': pair['check_time']
                            })
                    
                    # 确保有内容才发送邮件
                    if current_volatile_pairs:
                        print(f"\n正在发送价格异动邮件通知...共有{len(current_volatile_pairs)}个交易对符合条件")
                        subject = f"价格异动警报 - {len(current_volatile_pairs)}个交易对出现大幅波动"
                        try:
                            send_email(subject, email_content)
                            print("邮件发送成功!")
                        except Exception as e:
                            print(f"邮件发送失败: {str(e)}")
                            traceback.print_exc()
                    else:
                        print("\n没有符合条件的交易对，不发送邮件。")
                
                # 存储波动最大的交易对，用于API返回
                self.top_volatile_pairs = top_volatile_pairs  # 只存储真正符合条件的交易对
                
                # 更新K线ID
                if current_candle_id is not None:
                    self.last_candle_id = current_candle_id
                
                # 计算用时
                end_time = time.time()
                print(f"\n本轮检查用时: {end_time - start_time:.2f}秒")
                
                # 将波动交易对写入队列，用于前端显示
                if self.results_queue and self.top_volatile_pairs:
                    # 创建带时间戳的摘要数据
                    summary_data = {
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'top_pairs': self.top_volatile_pairs,
                        'time_period': self.time_period,
                        'volatility_threshold': self.volatility_threshold,
                        'monitor_direction': self.monitor_direction,
                    }
                    
                    try:
                        # 直接放入新数据而不清空队列，让API层决定如何处理
                        self.results_queue.put(summary_data)
                        print(f"已将{len(self.top_volatile_pairs)}个交易对数据添加到结果队列")
                    except Exception as e:
                        print(f"更新结果队列时出错: {str(e)}")
                
                # 等待下一次刷新
                refresh_time = max(1, self.refresh_interval)  # 确保至少有1秒的刷新间隔
                print(f"等待{refresh_time}秒后进行下一轮检查...")
                time.sleep(refresh_time)
                
        except Exception as e:
            print(f'{self.name}执行出错:', str(e))
            print(f"错误类型: {type(e).__name__}") 
            
    # 添加重试失败交易对的方法
    def _retry_failed_pairs(self, failed_pairs):
        """重试获取失败的交易对"""
        results = []
        retry_by_exchange = defaultdict(list)
        
        # 按交易所分组
        for pair in failed_pairs:
            retry_by_exchange[pair['source']].append(pair['symbol'])
            
        # 每个交易所分别处理
        for source, symbols in retry_by_exchange.items():
            print(f"重试 {source} 交易所的 {len(symbols)} 个交易对...")
            
            # 限制每批处理的交易对数量
            batch_size = 5 if source == "okx" else 10
            
            for i in range(0, len(symbols), batch_size):
                batch = symbols[i:i+batch_size]
                with ThreadPoolExecutor(max_workers=batch_size) as executor:
                    futures = {executor.submit(self.check_price_for_pair, symbol): symbol for symbol in batch}
                    
                    for future in as_completed(futures):
                        result = future.result()
                        if result:
                            result['check_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            results.append(result)
                
                # 每批之间添加延迟
                if source == "okx" and i + batch_size < len(symbols):
                    time.sleep(1.0)  # OKX交易所额外等待
                elif i + batch_size < len(symbols):
                    time.sleep(0.3)
        
        print(f"重试完成，成功获取 {len(results)}/{len(failed_pairs)} 个交易对数据")
        return results
            
    def stop(self):
        """停止策略执行"""
        self.is_running = False
        print(f"{self.name}已停止") 