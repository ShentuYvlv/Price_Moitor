import ccxt
import json
from datetime import datetime, timedelta
import time
import os
import pandas as pd
import traceback
from collections import defaultdict
from utils import (
    Strategy, get_socks5_proxy, get_bybit_perpetual_symbols, 
    send_email, fetch_market_data_batch, fetch_historical_data_batch,
    save_data_with_timestamp, combine_market_data, verify_funding_rates
)
"""
Bybit永续合约市场数据分析工具
获取资金费率以及价格，寻找机会。
目前这个脚本只支持bybit。
"""


class MarketDataStrategy(Strategy):
    """Bybit永续合约市场数据策略"""
    def __init__(self):
        super().__init__("Bybit永续合约市场数据策略")
        self.interval = 300  # 每300秒更新一次数据
        self.symbols = []  # 交易对列表
        self.market_data_history = {}  # 市场数据历史
        self.market_data_history_file = "market_data/market_data_history.json"
    
    def initialize(self):
        """初始化策略"""
        print(f'初始化{self.name}...')
        # 初始化Bybit交易所
        self.exchange = ccxt.bybit({
            'enableRateLimit': True,
            'timeout': 30000,
            'proxies': get_socks5_proxy(),
            'options': {
                'defaultType': 'swap',  # 设置为永续合约模式
                'recvWindow': 60000
            },
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        })
        
        # 创建结果目录
        os.makedirs("market_data", exist_ok=True)
        
        # 先加载市场数据
        print("正在加载市场数据...")
        self.exchange.load_markets()
        
        # 获取所有永续合约交易对
        self.symbols = get_bybit_perpetual_symbols(self.exchange)
        print(f'共加载了 {len(self.symbols)} 个永续合约交易对')
        
        # 加载历史市场数据
        self.load_market_data_history()
        
        self.is_running = True
        print(f'{self.name}初始化完成')
    
    def load_market_data_history(self):
        """加载历史市场数据"""
        try:
            if os.path.exists(self.market_data_history_file):
                with open(self.market_data_history_file, 'r', encoding='utf-8') as f:
                    self.market_data_history = json.load(f)
                print(f"已加载 {len(self.market_data_history)} 条历史市场数据记录")
            else:
                self.market_data_history = {}
                print("未找到历史市场数据文件，将创建新的记录")
        except Exception as e:
            print(f"加载历史市场数据时出错: {str(e)}")
            self.market_data_history = {}
    
    def save_market_data_history(self):
        """保存历史市场数据"""
        try:
            with open(self.market_data_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.market_data_history, f, indent=4)
            print(f"已保存历史市场数据到 {self.market_data_history_file}")
        except Exception as e:
            print(f"保存历史市场数据时出错: {str(e)}")
    
    def update_market_data_history(self, market_data):
        """更新市场数据历史
        
        Args:
            market_data: 当前市场数据列表
        """
        timestamp = str(int(time.time()))
        
        # 转换列表为以symbol为键的字典
        market_data_dict = {item['symbol']: item for item in market_data}
        
        # 更新历史数据
        self.market_data_history[timestamp] = market_data_dict
        
        # 清理超过24小时的数据
        cutoff_time = int(time.time()) - 86400  # 24小时
        self.market_data_history = {k: v for k, v in self.market_data_history.items() if int(k) > cutoff_time}
        
        # 保存更新后的历史数据
        self.save_market_data_history()
    
    def calculate_market_data_changes(self, current_data, hours=4):
        """计算指定小时前的市场数据变化
        
        Args:
            current_data: 当前市场数据列表
            hours: 对比的小时数
            
        Returns:
            list: 市场数据变化列表
        """
        now = int(time.time())
        target_time = now - (hours * 3600)  # 目标时间（小时前）
        
        # 转换当前数据为以symbol为键的字典
        current_data_dict = {item['symbol']: item for item in current_data}
        
        # 寻找最接近目标时间的数据点
        closest_timestamp = None
        for timestamp in self.market_data_history.keys():
            if int(timestamp) < target_time:
                if closest_timestamp is None or abs(int(timestamp) - target_time) < abs(int(closest_timestamp) - target_time):
                    closest_timestamp = timestamp
        
        if closest_timestamp is None:
            print(f"没有找到 {hours} 小时前的市场数据，无法计算变化")
            return []
            
        old_data = self.market_data_history[closest_timestamp]
        old_time = datetime.fromtimestamp(int(closest_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"正在对比当前市场数据与 {old_time} 的数据（约 {hours} 小时前）")
        
        # 计算变化
        changes = []
        for symbol, current in current_data_dict.items():
            if symbol in old_data:
                old = old_data[symbol]
                
                # 计算开仓量变化
                current_oi = current.get('open_interest', 0)
                old_oi = old.get('open_interest', 0)
                
                if current_oi is not None and old_oi is not None and old_oi > 0:
                    oi_change = current_oi - old_oi
                    oi_percent_change = (oi_change / old_oi) * 100
                else:
                    oi_change = 0
                    oi_percent_change = 0
                
                # 计算资金费率变化
                current_fr = current.get('funding_rate', 0)
                old_fr = old.get('funding_rate', 0)
                
                if current_fr is not None and old_fr is not None:
                    fr_change = current_fr - old_fr
                else:
                    fr_change = 0
                
                # 添加变化数据
                changes.append({
                    'symbol': symbol,
                    'current_oi': current_oi,
                    'old_oi': old_oi,
                    'oi_change': oi_change,
                    'oi_percent_change': oi_percent_change,
                    'current_fr': current_fr,
                    'old_fr': old_fr,
                    'fr_change': fr_change,
                    'price_change_percent': current.get('price_change_percent', 0)
                })
        
        return changes
    
    def analyze_data(self, market_data, market_changes):
        """分析和展示数据
        
        Args:
            market_data: 当前市场数据列表
            market_changes: 市场数据变化列表
            
        Returns:
            dict: 分析结果
        """
        print("\n==================== Bybit永续合约市场数据分析 ====================")
        print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 转换为DataFrame
        df_market = pd.DataFrame(market_data)
        df_changes = pd.DataFrame(market_changes) if market_changes else pd.DataFrame()
        
        # 按照价格变化百分比从高到低排序展示数据
        if not df_market.empty and 'price_change_percent' in df_market.columns:
            # 清除NaN值
            df_with_price = df_market.dropna(subset=['price_change_percent'])
            
            if not df_with_price.empty:
                # 按价格变化排序（从高到低）
                sorted_df = df_with_price.sort_values(by='price_change_percent', ascending=False)
                
                # 显示所有交易对数据，按价格变化排序
                print("\n===== 所有交易对按价格变化排序 =====")
                # 给symbol列分配更多空间，确保长符号能够完整显示
                print(f"{'交易对':<20}\t{'价格(4H)%':<10}\t{'当前价格':<5}\t{'上一价格':<10}\t{'资金费率':<5}")
                print("-" * 90)
                
                for _, row in sorted_df.iterrows():
                    symbol = row['symbol']
                    pct_change = row.get('price_change_percent', 'N/A')
                    current_price = row.get('current_price', 'N/A')
                    previous_price = row.get('previous_price', 'N/A')
                    funding_rate = row.get('funding_rate', 'N/A')
                    
                    # 格式化输出
                    pct_change_str = f"{pct_change:.2f}%" if pct_change != 'N/A' else 'N/A'
                    current_price_str = f"{current_price:.4f}" if current_price != 'N/A' else 'N/A'
                    previous_price_str = f"{previous_price:.4f}" if previous_price != 'N/A' else 'N/A'
                    funding_rate_str = f"{funding_rate:.6f}%" if funding_rate != 'N/A' else 'N/A'
                    
                    print(f"{symbol:<20}\t{pct_change_str:<10}\t{current_price_str:<15}\t{previous_price_str:<15}\t{funding_rate_str:<10}")
                
                # 潜在做多机会和做空机会分析
                if 'funding_rate' in df_with_price.columns:
                    # 找出价格上涨但资金费率为负的币种（可能的做多机会）
                    long_opportunity = df_with_price[(df_with_price['price_change_percent'] > 10) & (df_with_price['funding_rate'] < -0.01)]
                    if not long_opportunity.empty:
                        print("\n===== 潜在做多机会（价格上涨+负资金费率）=====")
                        for _, row in long_opportunity.sort_values(by='price_change_percent', ascending=False).iterrows():
                            symbol = row['symbol']
                            pct_change = row.get('price_change_percent', 'N/A')
                            current_price = row.get('current_price', 'N/A')
                            previous_price = row.get('previous_price', 'N/A')
                            funding_rate = row.get('funding_rate', 'N/A')
                            
                            # 格式化输出
                            pct_change_str = f"{pct_change:.2f}%" if pct_change != 'N/A' else 'N/A'
                            current_price_str = f"{current_price:.4f}" if current_price != 'N/A' else 'N/A'
                            previous_price_str = f"{previous_price:.4f}" if previous_price != 'N/A' else 'N/A'
                            funding_rate_str = f"{funding_rate:.6f}%" if funding_rate != 'N/A' else 'N/A'
                            
                            print(f"{symbol:<20}\t{pct_change_str:<10}\t{current_price_str:<15}\t{previous_price_str:<15}\t{funding_rate_str:<10}")
                    else:
                        print("\n未发现潜在做多机会")
                    
                    # 找出价格下跌但资金费率为正的币种（可能的做空机会）
                    short_opportunity = df_with_price[(df_with_price['price_change_percent'] < -10) & (df_with_price['funding_rate'] > 0.01)]
                    if not short_opportunity.empty:
                        print("\n===== 潜在做空机会（价格下跌+正资金费率）=====")
                        for _, row in short_opportunity.sort_values(by='price_change_percent', ascending=True).iterrows():
                            symbol = row['symbol']
                            pct_change = row.get('price_change_percent', 'N/A')
                            current_price = row.get('current_price', 'N/A')
                            previous_price = row.get('previous_price', 'N/A')
                            funding_rate = row.get('funding_rate', 'N/A')
                            
                            # 格式化输出
                            pct_change_str = f"{pct_change:.2f}%" if pct_change != 'N/A' else 'N/A'
                            current_price_str = f"{current_price:.4f}" if current_price != 'N/A' else 'N/A'
                            previous_price_str = f"{previous_price:.4f}" if previous_price != 'N/A' else 'N/A'
                            funding_rate_str = f"{funding_rate:.6f}%" if funding_rate != 'N/A' else 'N/A'
                            
                            print(f"{symbol:<20}\t{pct_change_str:<10}\t{current_price_str:<15}\t{previous_price_str:<15}\t{funding_rate_str:<10}")
                    else:
                        print("\n未发现潜在做空机会")
                
                # 构建分析结果
                return {
                    'market_data': market_data,
                    'market_changes': df_changes.to_dict('records') if not df_changes.empty else [],
                    'price_data': sorted_df.to_dict('records'),
                    'market_trend': {
                        'long_opportunities': long_opportunity['symbol'].tolist() if not long_opportunity.empty else [],
                        'short_opportunities': short_opportunity['symbol'].tolist() if not short_opportunity.empty else []
                    }
                }
        
        # 如果没有价格变化数据，返回基本结果
        return {
            'market_data': market_data,
            'market_changes': df_changes.to_dict('records') if not df_changes.empty else [],
            'market_trend': {}
        }
    
    def execute(self):
        """执行策略"""
        try:
            while self.is_running:
                start_time = time.time()
                print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始获取市场数据...")
                
                # 1. 获取最新的交易对列表
                print("更新交易对列表...")
                self.exchange.load_markets()
                new_symbols = get_bybit_perpetual_symbols(self.exchange)
                if len(new_symbols) != len(self.symbols):
                    print(f"交易对列表已更新: {len(self.symbols)} -> {len(new_symbols)}")
                    self.symbols = new_symbols
                
                # 验证资金费率数据（调试用，默认注释）
                # import random
                # debug_symbols = random.sample(self.symbols, min(10, len(self.symbols)))  # 随机抽取交易对
                # verify_funding_rates(self.exchange, debug_symbols)
                
                # 2. 使用多线程批量获取所有市场数据（包含资金费率、当前开仓量和价格变化）
                print(f"使用多线程批量获取 {len(self.symbols)} 个交易对的完整市场数据...")
                # 使用更高效的批处理机制和优化参数获取数据
                market_data = fetch_market_data_batch(
                    self.exchange, 
                    self.symbols, 
                    timeframe='4h', 
                    limit=2, 
                    max_workers=100,    # 使用更多线程
                    timeout=15,          # 设置请求超时时间
                    retries=3,           # 添加重试次数
                    batch_size=200       # 设置批处理大小
                )
                
                # 3. 更新市场数据历史
                self.update_market_data_history(market_data)
                
                # 4. 计算市场数据变化（主要是开仓量变化）
                market_changes = self.calculate_market_data_changes(market_data, hours=4)
                
                # 5. 分析数据
                analysis_data = self.analyze_data(market_data, market_changes)
                
                # 6. 保存分析结果
                analysis_data_with_timestamp = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'data': analysis_data
                }
                
                # 保存分析数据
                #save_data_with_timestamp(analysis_data_with_timestamp, "market_data", "market_analysis")
                
                # 检查是否有机会需要通知
                opportunities = []
                if 'market_trend' in analysis_data:
                    long_opportunities = analysis_data['market_trend'].get('long_opportunities', [])
                    short_opportunities = analysis_data['market_trend'].get('short_opportunities', [])
                    
                    if long_opportunities:
                        opportunities.extend(long_opportunities)
                    if short_opportunities:
                        opportunities.extend(short_opportunities)
                
                # 如果有机会，发送邮件通知
                if opportunities and len(opportunities) >= 3:  # 至少3个交易机会
                    # 构建邮件内容
                    email_content = self.build_email_content(analysis_data)
                    
                    # 发送邮件
                    subject = f"【Bybit市场数据】发现{len(opportunities)}个潜在交易机会"
                    send_email(subject, email_content)
                    print(f"已发送市场数据机会邮件通知，包含{len(opportunities)}个潜在交易机会")
                
                # 等待下一轮
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"\n本轮数据获取用时: {execution_time:.2f}秒")
                
                wait_time = max(0, self.interval - execution_time)
                if wait_time > 0:
                    print(f"等待{wait_time:.1f}秒后继续下一轮数据获取...")
                    time.sleep(wait_time)
                
        except KeyboardInterrupt:
            print("\n收到中断信号，正在停止...")
        except Exception as e:
            print(f'{self.name}执行出错:', str(e))
            print(f"错误类型: {type(e).__name__}")
            traceback.print_exc()
    
    def build_email_content(self, analysis_data):
        """构建邮件通知内容
        
        Args:
            analysis_data: 分析结果数据
        
        Returns:
            str: 邮件内容
        """
        if not analysis_data or 'market_data' not in analysis_data:
            return "未发现市场数据"
        
        # 提取交易机会数据
        market_trend = analysis_data.get('market_trend', {})
        long_opportunities = market_trend.get('long_opportunities', [])
        short_opportunities = market_trend.get('short_opportunities', [])
        
        # 提取价格数据（按价格变化排序）
        price_data = []
        if 'price_data' in analysis_data:
            price_data = analysis_data['price_data']
        
        # 构建邮件内容
        content = "Bybit永续合约市场数据分析报告:\n\n"
        
        # 添加潜在交易机会
        if long_opportunities or short_opportunities:
            content += "===== 潜在交易机会 =====\n\n"
            
            # 添加做多机会
            if long_opportunities:
                content += "做多机会（价格上涨+负资金费率）:\n"
                
                # 从price_data中提取详细信息
                for symbol in long_opportunities:
                    for item in price_data:
                        if item.get('symbol') == symbol:
                            pct_change = item.get('price_change_percent', 'N/A')
                            funding_rate = item.get('funding_rate', 'N/A')
                            current_price = item.get('current_price', 'N/A')
                            
                            pct_change_str = f"{pct_change:.2f}%" if isinstance(pct_change, (int, float)) else 'N/A'
                            funding_rate_str = f"{funding_rate:.6f}%" if isinstance(funding_rate, (int, float)) else 'N/A'
                            current_price_str = f"{current_price:.4f}" if isinstance(current_price, (int, float)) else 'N/A'
                            
                            content += f"{symbol}: 价格变化 {pct_change_str}, 资金费率 {funding_rate_str}, 现价 {current_price_str}\n"
                            break
                
                content += "\n"
            
            # 添加做空机会
            if short_opportunities:
                content += "做空机会（价格下跌+正资金费率）:\n"
                
                # 从price_data中提取详细信息
                for symbol in short_opportunities:
                    for item in price_data:
                        if item.get('symbol') == symbol:
                            pct_change = item.get('price_change_percent', 'N/A')
                            funding_rate = item.get('funding_rate', 'N/A')
                            current_price = item.get('current_price', 'N/A')
                            
                            pct_change_str = f"{pct_change:.2f}%" if isinstance(pct_change, (int, float)) else 'N/A'
                            funding_rate_str = f"{funding_rate:.6f}%" if isinstance(funding_rate, (int, float)) else 'N/A'
                            current_price_str = f"{current_price:.4f}" if isinstance(current_price, (int, float)) else 'N/A'
                            
                            content += f"{symbol}: 价格变化 {pct_change_str}, 资金费率 {funding_rate_str}, 现价 {current_price_str}\n"
                            break
                
                content += "\n"
        else:
            content += "未发现潜在交易机会\n\n"
        
        # 添加价格变化排名靠前的币种
        if price_data:
            # 提取价格上涨最多的前10个
            content += "===== 价格上涨排名（Top 10）=====\n"
            sorted_by_price = sorted(price_data, key=lambda x: x.get('price_change_percent', 0) if x.get('price_change_percent') is not None else 0, reverse=True)
            for item in sorted_by_price[:10]:
                symbol = item.get('symbol', '')
                pct_change = item.get('price_change_percent', 'N/A')
                current_price = item.get('current_price', 'N/A')
                
                pct_change_str = f"{pct_change:.2f}%" if isinstance(pct_change, (int, float)) else 'N/A'
                current_price_str = f"{current_price:.4f}" if isinstance(current_price, (int, float)) else 'N/A'
                
                content += f"{symbol}: 价格变化 {pct_change_str}, 现价 {current_price_str}\n"
            
            content += "\n"
            
            # 提取价格下跌最多的前10个
            content += "===== 价格下跌排名（Top 10）=====\n"
            sorted_by_price_desc = sorted(price_data, key=lambda x: x.get('price_change_percent', 0) if x.get('price_change_percent') is not None else 0)
            for item in sorted_by_price_desc[:10]:
                symbol = item.get('symbol', '')
                pct_change = item.get('price_change_percent', 'N/A')
                current_price = item.get('current_price', 'N/A')
                
                pct_change_str = f"{pct_change:.2f}%" if isinstance(pct_change, (int, float)) else 'N/A'
                current_price_str = f"{current_price:.4f}" if isinstance(current_price, (int, float)) else 'N/A'
                
                content += f"{symbol}: 价格变化 {pct_change_str}, 现价 {current_price_str}\n"
        
        return content

if __name__ == '__main__':
    try:
        print('CCXT 版本:', ccxt.__version__)
        
        # 创建并运行市场数据策略
        strategy = MarketDataStrategy()
        strategy.initialize()
        strategy.execute()
        
    except KeyboardInterrupt:
        print('\n程序已停止运行') 