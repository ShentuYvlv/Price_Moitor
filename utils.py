import ccxt
import json
import os
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
import pandas as pd
import random

# 邮箱配置
SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 587
EMAIL_ADDRESS = '1833429505@qq.com'
EMAIL_PASSWORD = 'igzowcjvsdkhehdh'
RECIPIENT_EMAIL = '1833429505@qq.com'

def get_socks5_proxy():
    """获取SOCKS5代理配置"""
    return {
        'http': 'socks5://127.0.0.1:10808',
        'https': 'socks5://127.0.0.1:10808'
    }

def send_email(subject, content):
    """发送邮件的函数"""
    try:
        html = '<html>'
        html += '<head>'
        html += '<style>'
        html += '''
            body {
                font-family: "Microsoft YaHei", Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background-color: #1a73e8;
                color: white;
                padding: 20px;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
            }
            .alert-box {
                padding: 20px;
                line-height: 1.8;
            }
            .info-item {
                margin: 15px 0;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            .pair-box {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                background-color: white;
                transition: all 0.3s ease;
            }
            .pair-box:hover {
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transform: translateY(-2px);
            }
            .symbol {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
            .up {
                color: #00c853;
                font-weight: bold;
            }
            .down {
                color: #ff1744;
                font-weight: bold;
            }
            .change {
                font-size: 14px;
                color: #666;
                margin-left: 5px;
            }
            .footer {
                text-align: center;
                padding: 15px;
                color: #666;
                font-size: 12px;
                border-top: 1px solid #eee;
                margin-top: 20px;
            }
            .volatility {
                display: flex;
                gap: 20px;
                margin-top: 10px;
            }
            .volatility-item {
                flex: 1;
            }
        '''
        html += '</style>'
        html += '</head>'
        html += '<body>'
        html += '<div class="container">'
        html += f'<div class="header">🔔 {subject}</div>'
        html += '<div class="alert-box">'
        
        # 处理内容
        lines = content.strip().split('\n')
        html += '<div class="info-item">'
        
        # 跳过第一行的标题
        for line in lines[2:]:  # 跳过"发现大波动交易对:"和空行
            if not line.strip():
                continue
                
            # 解析行内容
            if ':' in line:
                symbol, data = line.split(':', 1)
                symbol = symbol.strip()
                data = data.strip()
                
                html += '<div class="pair-box">'
                html += f'<div class="symbol">{symbol}</div>'
                html += '<div class="volatility">'
                
                # 处理上涨数据
                if '上涨' in data:
                    up_part = data.split('下跌')[0]
                    up_value = up_part.split('上涨')[1].split('%')[0].strip()
                    html += '<div class="volatility-item">'
                    html += f'上涨 <span class="up">{up_value}%</span>'
                    
                    # 处理上涨变化值
                    if '变化:' in up_part:
                        change = up_part.split('变化:')[1].split('%')[0].strip()
                        html += f'<span class="change">(变化: {change}%)</span>'
                    html += '</div>'
                
                # 处理下跌数据
                if '下跌' in data:
                    down_part = data.split('下跌')[1]
                    down_value = down_part.split('%')[0].strip()
                    html += '<div class="volatility-item">'
                    html += f'下跌 <span class="down">{down_value}%</span>'
                    
                    # 处理下跌变化值
                    if '变化:' in down_part:
                        change = down_part.split('变化:')[1].split('%')[0].strip()
                        html += f'<span class="change">(变化: {change}%)</span>'
                    html += '</div>'
                
                html += '</div></div>'
        
        html += '</div>'
        html += '</div>'
        html += '<div class="footer">此邮件由价格监控系统自动发送</div>'
        html += '</div>'
        html += '</body>'
        html += '</html>'

        msg = MIMEText(html, 'html', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
            print(f"邮件发送成功: {subject}")
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        return

def get_perpetual_symbols(exchange):
    """获取所有USDT永续合约交易对的symbol"""
    # 加载市场数据
    markets = exchange.load_markets()
    
    # 获取所有USDT永续合约交易对的symbol
    perpetual_symbols = [
        symbol for symbol, market in markets.items()
        if market['quote'] == 'USDT' and market['linear'] and not market.get('expiry')
    ]
    
    return perpetual_symbols

def save_perpetual_symbols(symbols, filename='perpetual_symbols.json'):
    """保存永续合约交易对列表到文件"""
    with open(filename, 'w') as f:
        json.dump(symbols, f, indent=4)

def load_perpetual_symbols(filename='perpetual_symbols.json'):
    """从JSON文件加载永续合约交易对列表"""
    try:
        if not os.path.exists(filename):
            return []
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取{filename}时出错: {str(e)}")
        return []

def get_price_data(exchange, symbol, timeframe='5m'):
    """获取指定交易对的价格数据"""
    try:
        # 获取K线数据，只需要最新的一条
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=1)
        if not ohlcv:
            return None
            
        # 解析数据
        timestamp = ohlcv[0][0]
        open_price = ohlcv[0][1]
        high_price = ohlcv[0][2]
        low_price = ohlcv[0][3]
        close_price = ohlcv[0][4]
        
        # 计算波动幅度
        up_volatility = ((high_price - open_price) / open_price) * 100
        down_volatility = ((low_price - open_price) / open_price) * 100
        
        return {
            'symbol': symbol,
            'open_price': open_price,
            'high_price': high_price,
            'low_price': low_price,
            'close_price': close_price,
            'up_vol': up_volatility,
            'down_vol': down_volatility,
            'timestamp': timestamp  # 添加K线时间戳
        }
    except Exception as e:
        # print(f"获取{symbol}数据时出错: {str(e)}")
        return None

def check_price_task(exchange, symbol):
    """线程任务：检查单个交易对的价格"""
    return get_price_data(exchange, symbol)

def get_candle_id(timestamp):
    """根据时间戳获取5分钟K线的唯一标识"""
    dt = datetime.fromtimestamp(timestamp / 1000)
    # 5分钟K线的ID：小时*12 + 分钟/5
    return dt.hour * 12 + dt.minute // 5

def find_previous_volatility(symbol, volatile_pairs):
    """在当前已记录的波动中查找指定交易对的记录"""
    for pair in volatile_pairs:
        if pair['symbol'] == symbol:
            return pair
    return None

def get_bybit_perpetual_symbols(exchange):
    """获取Bybit所有USDT永续合约交易对的symbol"""
    try:
        # 获取所有USDT永续合约交易对的symbol
        perpetual_symbols = []
        
        # 确保使用合约市场
        markets = exchange.markets
        
        for symbol, market in markets.items():
            # 确保是USDT交易对且是线性合约且不是期货
            if ('quote' in market and market['quote'] == 'USDT' and 
                market.get('linear', False) and 
                market.get('type', '') == 'swap' and  # 确保是永续合约
                not market.get('expiry')):
                perpetual_symbols.append(symbol)
        
        return perpetual_symbols
    except Exception as e:
        print(f"获取永续合约交易对时出错: {str(e)}")
        traceback.print_exc()
        return []

def fetch_funding_rates(exchange, symbols):
    """获取资金费率数据"""
    try:
        # 验证交易对列表
        valid_symbols = []
        for symbol in symbols:
            try:
                market = exchange.market(symbol)
                if market.get('linear', False) and market.get('type', '') == 'swap':
                    valid_symbols.append(symbol)
            except Exception:
                continue
            
        print(f"正在获取 {len(valid_symbols)} 个有效的永续合约交易对的资金费率...")
        
        # 尝试使用批量请求方式获取（默认最多50个一批）
        try:
            exchange.options['defaultType'] = 'swap'
            # 首先尝试批量获取
            print("尝试批量获取资金费率...")
            funding_rates = {}
            
            # 分批处理，每批最多20个
            batch_size = 20
            total_batches = (len(valid_symbols) + batch_size - 1) // batch_size
            
            for i in range(0, len(valid_symbols), batch_size):
                batch = valid_symbols[i:i+batch_size]
                print(f"处理批次 {i//batch_size + 1}/{total_batches} ({len(batch)}个交易对)")
                try:
                    # 尝试获取一批交易对的资金费率
                    batch_rates = exchange.fetch_funding_rates(symbols=batch)
                    if batch_rates:
                        funding_rates.update(batch_rates)
                except Exception as e:
                    print(f"批量获取失败: {str(e)}，将切换到单个获取模式")
                    # 批量获取失败，则单个获取该批次
                    for symbol in batch:
                        try:
                            result = exchange.fetch_funding_rate(symbol)
                            if result and 'fundingRate' in result:
                                funding_rates[symbol] = result
                        except Exception as e:
                            print(f"获取 {symbol} 失败: {str(e)}")
                        
                # 避免请求过快
                time.sleep(0.5)
                
            success_count = sum(1 for _, rate in funding_rates.items() if 'fundingRate' in rate)
            print(f"成功获取 {success_count} 个交易对的资金费率")
            return funding_rates
            
        except Exception as e:
            print(f"批量获取失败，切换到单个获取模式: {str(e)}")
            # 批量模式失败，回退到单个获取
        
        # 单独获取每个交易对的资金费率
        funding_rates = {}
        success_count = 0
        total = len(valid_symbols)
        
        print("开始单个获取资金费率...")
        for i, symbol in enumerate(valid_symbols):
            try:
                # 显示进度
                if i % 10 == 0 or i == total - 1:
                    print(f"进度: {i+1}/{total} ({(i+1)/total*100:.1f}%)")
                
                # 确保使用正确的市场类型
                exchange.options['defaultType'] = 'swap'
                result = exchange.fetch_funding_rate(symbol)
                if result and 'fundingRate' in result:
                    funding_rates[symbol] = result
                    success_count += 1
                
                # 加入延迟避免请求过快 - 调整延迟时间
                if i % 10 == 9:  # 每10个请求暂停一下
                    time.sleep(0.5)
                else:
                    time.sleep(0.05)  # 缩短单次延迟
                    
            except Exception as e:
                # 仅记录错误，继续处理下一个
                if "rate limit" in str(e).lower():
                    print(f"触发速率限制，暂停3秒...")
                    time.sleep(3)  # 触发限制时多等待
                    
        print(f"成功获取 {success_count} 个交易对的资金费率")
        return funding_rates
    except Exception as e:
        print(f"获取资金费率数据时出错: {str(e)}")
        traceback.print_exc()
        return {}

def fetch_positions(exchange, api_key, api_secret):
    """获取当前持仓数据"""
    try:
        if not api_key or not api_secret:
            print("警告: 未配置API密钥，无法获取持仓数据")
            return []
            
        print("正在获取当前持仓数据...")
        positions = exchange.fetch_positions()
        
        # 只保留有持仓的交易对
        active_positions = [p for p in positions if abs(float(p.get('contracts', 0))) > 0]
        
        print(f"当前有 {len(active_positions)} 个活跃持仓")
        return active_positions
        
    except Exception as e:
        print(f"获取持仓数据时出错: {str(e)}")
        traceback.print_exc()
        return []

def load_json_data(filepath):
    """从JSON文件加载数据"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"加载数据时出错: {str(e)}")
        return {}

def save_json_data(data, filepath):
    """保存数据到JSON文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"数据已保存至 {filepath}")
        return True
    except Exception as e:
        print(f"保存数据时出错: {str(e)}")
        return False

def save_data_with_timestamp(data, directory, filename_prefix):
    """保存带时间戳的数据到文件"""
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f"{directory}/{filename_prefix}_{timestamp}.json"
    
    return save_json_data(data, filepath)

class Strategy(ABC):
    """策略基类"""
    def __init__(self, name):
        self.name = name
        self.exchange = None
        self.is_running = False
    
    @abstractmethod
    def initialize(self):
        """初始化策略"""
        pass
    
    @abstractmethod
    def execute(self):
        """执行策略"""
        pass
    
    def stop(self):
        """停止策略"""
        self.is_running = False

def fetch_market_data(exchange, symbol, timeframe='4h', limit=2):
    """获取单个交易对的全部市场数据，同时包括资金费率、开仓量和价格变化
    
    Args:
        exchange: CCXT交易所实例
        symbol: 交易对符号
        timeframe: 时间周期
        limit: 获取历史价格数据的数量
        
    Returns:
        dict: 交易对的完整市场数据
    """
    try:
        result = {
            'symbol': symbol,
            'funding_rate': None,
            'open_interest': None,
            'open_interest_amount': None,
            'current_price': None,
            'previous_price': None,
            'price_change_percent': None,
            'timestamp': int(time.time() * 1000)
        }
        
        # 一次性获取所有数据类型
        # 1. 获取价格变化（当前和历史价格）- 最关键的数据
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            if len(ohlcv) >= 2:
                # 当前和历史的数据
                current = ohlcv[-1]
                previous = ohlcv[0]
                
                result['current_price'] = current[4]  # 收盘价
                result['previous_price'] = previous[1]  # 开盘价
                
                # 计算价格变化百分比
                if previous[1] != 0:
                    result['price_change_percent'] = ((current[4] - previous[1]) / previous[1]) * 100
        except Exception as e:
            print(f"获取{symbol}价格数据失败: {str(e)}")
            
        # 2. 获取资金费率 - 尝试三种方式获取，确保数据准确性
        try:
            # 方式1: 直接获取funding_rate
            funding_data = None
            try:
                funding_data = exchange.fetch_funding_rate(symbol)
                if funding_data and 'fundingRate' in funding_data:
                    funding_rate = funding_data['fundingRate']
                    # Bybit资金费率通常是以小数形式表示，如0.0001 = 0.01%
                    result['funding_rate'] = funding_rate * 100  # 转为百分比
                    # 调试信息
                    # print(f"DEBUG - {symbol} 资金费率: {funding_rate} -> {result['funding_rate']}%")
            except Exception as e:
                print(f"方式1获取{symbol}资金费率失败: {str(e)}")
            
            # 方式2: 如果第一种方式失败，尝试使用ticker获取
            if result['funding_rate'] is None:
                try:
                    ticker = exchange.fetch_ticker(symbol)
                    if ticker and 'info' in ticker:
                        info = ticker['info']
                        if 'fundingRate' in info:
                            funding_rate = float(info['fundingRate'])
                            result['funding_rate'] = funding_rate * 100
                            # print(f"DEBUG(方式2) - {symbol} 资金费率: {funding_rate} -> {result['funding_rate']}%")
                except Exception as e:
                    print(f"方式2获取{symbol}资金费率失败: {str(e)}")
            
            # 方式3: 尝试使用市场信息获取
            if result['funding_rate'] is None:
                try:
                    market = exchange.market(symbol)
                    if market and 'info' in market and 'fundingRate' in market['info']:
                        funding_rate = float(market['info']['fundingRate'])
                        result['funding_rate'] = funding_rate * 100
                        # print(f"DEBUG(方式3) - {symbol} 资金费率: {funding_rate} -> {result['funding_rate']}%")
                except Exception as e:
                    pass  # 静默失败，因为这是最后一次尝试
        except Exception as e:
            print(f"获取{symbol}资金费率全部方式失败: {str(e)}")
            
        # 3. 获取持仓量
        try:
            # 由于看到很多交易对的持仓量数据为null，我们直接优先使用Bybit的专用API
            try:
                # 直接使用Bybit API v5获取持仓量 - 作为首选方法
                # 移除USDT:USDT后缀以匹配API格式
                base_symbol = symbol.split(':')[0] if ':' in symbol else symbol
                # 示例: BTC/USDT:USDT -> BTCUSDT
                clean_symbol = base_symbol.replace('/', '')  # 移除/符号
                
                # 使用Bybit v5 API直接获取持仓量
                endpoint = 'v5/market/open-interest'
                params = {
                    'category': 'linear',
                    'symbol': clean_symbol,
                    'intervalTime': '4h',
                    'limit': 1
                }
                
                try:
                    # 尝试直接调用Bybit API
                    response = exchange.public_get_market_open_interest(params)
                    
                    if response and 'result' in response and 'list' in response['result'] and len(response['result']['list']) > 0:
                        data = response['result']['list'][0]
                        if 'openInterest' in data and data['openInterest']:
                            result['open_interest'] = float(data['openInterest'])
                            
                            # 如果API直接提供了时间戳
                            if 'timestamp' in data:
                                result['open_interest_timestamp'] = int(data['timestamp'])
                            else:
                                result['open_interest_timestamp'] = int(time.time() * 1000)
                            
                            # 如果API返回了价格，计算持仓量价值
                            if 'price' in data and data['price']:
                                current_price = float(data['price'])
                                result['open_interest_amount'] = result['open_interest'] * current_price
                            elif result['current_price'] is not None:
                                # 使用已经获取的当前价格
                                result['open_interest_amount'] = result['open_interest'] * result['current_price']
                except Exception as e:
                    # print(f"Bybit专用API获取{symbol}持仓量失败: {str(e)}")
                    pass
                
                # 如果以上方法失败，则尝试通过公共endpoint获取
                if result['open_interest'] is None:
                    try:
                        response = exchange.request(
                            path=f'v5/market/open-interest',
                            api='public',
                            method='GET',
                            params=params
                        )
                        
                        if response and 'result' in response and 'list' in response['result'] and len(response['result']['list']) > 0:
                            data = response['result']['list'][0]
                            if 'openInterest' in data and data['openInterest']:
                                result['open_interest'] = float(data['openInterest'])
                                
                                # 获取时间戳
                                if 'timestamp' in data:
                                    result['open_interest_timestamp'] = int(data['timestamp'])
                                else:
                                    result['open_interest_timestamp'] = int(time.time() * 1000)
                                
                                # 计算持仓量价值
                                if 'price' in data and data['price']:
                                    current_price = float(data['price'])
                                    result['open_interest_amount'] = result['open_interest'] * current_price
                                elif result['current_price'] is not None:
                                    # 使用已经获取的当前价格
                                    result['open_interest_amount'] = result['open_interest'] * result['current_price']
                    except Exception as e:
                        # print(f"Bybit公共API获取{symbol}持仓量失败: {str(e)}")
                        pass
            except Exception as e:
                # print(f"Bybit特定API获取{symbol}持仓量出错: {str(e)}")
                pass

            # 如果上述Bybit特定方法失败，尝试标准CCXT方法
            if result['open_interest'] is None:
                try:
                    # 方式1: 通过CCXT标准方法获取持仓量
                    open_interest = exchange.fetch_open_interest(symbol)
                    if open_interest and open_interest.get('openInterest') is not None:
                        result['open_interest'] = open_interest.get('openInterest')
                        result['open_interest_amount'] = open_interest.get('openInterestAmount')
                        
                        # 如果没有直接获取到持仓量价值，使用持仓量和当前价格计算
                        if result['open_interest_amount'] is None and result['current_price'] is not None:
                            result['open_interest_amount'] = result['open_interest'] * result['current_price']
                        
                        # 获取时间戳以便记录持仓量历史
                        if 'timestamp' in open_interest:
                            result['open_interest_timestamp'] = open_interest.get('timestamp')
                        else:
                            result['open_interest_timestamp'] = int(time.time() * 1000)
                except Exception as e:
                    # print(f"CCXT标准方法获取{symbol}持仓量失败: {str(e)}")
                    pass
                    
            # 如果方式1失败，尝试方式2: 通过ticker获取持仓量
            if result['open_interest'] is None:
                try:
                    ticker = exchange.fetch_ticker(symbol)
                    if ticker and 'info' in ticker:
                        info = ticker['info']
                        if 'openInterest' in info and info['openInterest']:
                            result['open_interest'] = float(info['openInterest'])
                            # 尝试获取或计算持仓量价值
                            if 'openInterestValue' in info:
                                result['open_interest_amount'] = float(info['openInterestValue'])
                            elif 'openInterestAmount' in info:
                                result['open_interest_amount'] = float(info['openInterestAmount'])
                            elif 'lastPrice' in info and info['lastPrice']:
                                # 使用最新价格计算
                                result['open_interest_amount'] = result['open_interest'] * float(info['lastPrice'])
                            elif result['current_price'] is not None:
                                # 使用已经获取的当前价格
                                result['open_interest_amount'] = result['open_interest'] * result['current_price']
                            
                            result['open_interest_timestamp'] = int(time.time() * 1000)
                except Exception as e:
                    # print(f"Ticker方法获取{symbol}持仓量失败: {str(e)}")
                    pass
            
            # 如果上述方法都失败，尝试方式4: 通过Tickers Bulk API
            if result['open_interest'] is None and result['current_price'] is not None:
                try:
                    # 通过当前价格和交易量近似计算
                    current_price = result['current_price']
                    
                    # 获取24小时成交量数据
                    ticker_info = exchange.fetch_ticker(symbol)
                    if ticker_info and ticker_info.get('quoteVolume') and ticker_info['quoteVolume'] > 0:
                        # 在某些交易所中，持仓量与24小时成交量有一定关系
                        # 这是一个近似值，不是准确的持仓量，但可以作为备选
                        volume_24h = float(ticker_info['quoteVolume'])
                        # 以成交量的一定比例作为持仓量的估计值（例如50%）
                        estimated_oi_amount = volume_24h * 0.5
                        result['open_interest_amount'] = estimated_oi_amount
                        result['open_interest'] = estimated_oi_amount / current_price
                        result['open_interest_timestamp'] = int(time.time() * 1000)
                        result['open_interest_is_estimated'] = True  # 标记为估计值
                except Exception as e:
                    # print(f"估计{symbol}持仓量失败: {str(e)}")
                    pass
                    
            # 在所有方法尝试后，如果仍然没有持仓量数据，可以添加一个标志
            if result['open_interest'] is None:
                result['open_interest_available'] = False
            else:
                result['open_interest_available'] = True
                
                # 确保持仓量价值正确计算
                if result['open_interest_amount'] is None and result['current_price'] is not None:
                    result['open_interest_amount'] = result['open_interest'] * result['current_price']
                
        except Exception as e:
            # 持仓量获取失败不影响其他数据获取
            # print(f"获取{symbol}持仓量失败: {str(e)}")
            result['open_interest_available'] = False
            
        return result
    except Exception as e:
        print(f"获取{symbol}数据时错误: {str(e)}")
        # 如果整体获取失败，至少返回交易对符号
        return {'symbol': symbol}

def fetch_market_data_batch(exchange, symbols, timeframe='4h', limit=2, max_workers=30, timeout=10, retries=2, batch_size=200):
    """并发获取多个交易对的完整市场数据
    
    Args:
        exchange: CCXT交易所实例
        symbols: 交易对符号列表
        timeframe: 时间周期
        limit: 获取历史价格数据的数量
        max_workers: 最大线程数
        timeout: 请求超时时间(秒)
        retries: 请求失败重试次数
        batch_size: 每批处理的交易对数量，避免一次创建过多线程
        
    Returns:
        list: 所有交易对的完整市场数据列表
    """
    results = []
    all_completed = 0
    all_total = len(symbols)
    
    # 如果符号列表为空，直接返回空结果
    if not symbols:
        print("警告: 交易对列表为空，无法获取市场数据")
        return []
    
    print(f"开始批量获取{all_total}个交易对的完整市场数据 (最大线程数: {max_workers}, 超时: {timeout}秒, 重试: {retries}次)...")
    total_start_time = time.time()
    
    # 将交易对分批处理，避免一次创建过多线程
    batches = [symbols[i:i+batch_size] for i in range(0, len(symbols), batch_size)]
    
    for batch_idx, batch_symbols in enumerate(batches):
        batch_size = len(batch_symbols)
        print(f"\n处理批次 {batch_idx+1}/{len(batches)} ({batch_size}个交易对)...")
        batch_results = []
        completed = 0
        
        batch_start_time = time.time()
        
        # 定义包含重试逻辑的工作函数
        def fetch_with_retry(exchange, symbol, timeframe, limit, max_retries):
            for attempt in range(max_retries + 1):
                try:
                    # 设置超时
                    exchange.options['timeout'] = timeout * 1000  # 毫秒
                    result = fetch_market_data(exchange, symbol, timeframe, limit)
                    return result
                except Exception as e:
                    if attempt < max_retries:
                        # 指数退避重试
                        sleep_time = 0.5 * (2 ** attempt)
                        # print(f"获取{symbol}数据失败，{sleep_time:.1f}秒后重试 ({attempt+1}/{max_retries}): {str(e)}")
                        time.sleep(sleep_time)
                    else:
                        print(f"获取{symbol}数据失败，已达最大重试次数: {str(e)}")
                        return {'symbol': symbol}  # 返回最小信息
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 为每个交易对创建一个任务，获取其所有相关数据
            futures = {
                executor.submit(
                    fetch_with_retry, exchange, symbol, timeframe, limit, retries
                ): symbol for symbol in batch_symbols
            }
            
            for future in as_completed(futures):
                symbol = futures[future]
                try:
                    result = future.result()
                    if result and 'symbol' in result:
                        batch_results.append(result)
                except Exception as e:
                    print(f"获取{symbol}数据失败: {str(e)}")
                
                completed += 1
                all_completed += 1
                
                # 计算进度和预计剩余时间
                if completed % 5 == 0 or completed == batch_size:
                    elapsed = time.time() - batch_start_time
                    batch_progress = completed / batch_size
                    all_progress = all_completed / all_total
                    
                    # 计算预计剩余时间
                    if batch_progress > 0:
                        batch_eta = (elapsed / batch_progress) * (1 - batch_progress)
                        all_eta = (time.time() - total_start_time) / all_progress * (1 - all_progress)
                        print(f"\r批次进度: {completed}/{batch_size} ({batch_progress*100:.1f}%) "
                              f"- 批次剩余: {batch_eta:.1f}秒 | "
                              f"总进度: {all_completed}/{all_total} ({all_progress*100:.1f}%) "
                              f"- 总剩余: {all_eta:.1f}秒", end="")
                    else:
                        print(f"\r批次进度: {completed}/{batch_size} ({batch_progress*100:.1f}%) | "
                              f"总进度: {all_completed}/{all_total} ({all_progress*100:.1f}%)", end="")
        
        print(f"\n批次 {batch_idx+1} 完成，获取了 {len(batch_results)}/{batch_size} 个交易对的数据，用时: {time.time() - batch_start_time:.2f}秒")
        
        # 合并结果
        results.extend(batch_results)
        
        # 批次之间稍微暂停，避免API限制
        if batch_idx < len(batches) - 1:
            time.sleep(1)
    
    total_elapsed = time.time() - total_start_time
    success_rate = len(results) / all_total * 100 if all_total > 0 else 0
    
    print(f"\n完成获取市场数据, 总用时: {total_elapsed:.2f}秒, 成功获取: {len(results)}/{all_total} (成功率: {success_rate:.1f}%)")
    return results

def fetch_historical_open_interest(exchange, symbol, timeframe='4h', limit=2):
    """获取交易对的历史持仓量数据
    
    Args:
        exchange: CCXT交易所实例
        symbol: 交易对符号
        timeframe: 时间周期
        limit: 获取数量
        
    Returns:
        dict: 历史持仓量数据
    """
    try:
        # 获取历史持仓量数据
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if len(ohlcv) < 2:
            return None
            
        # 当前和4小时前的数据
        current = ohlcv[-1]
        previous = ohlcv[0]
        
        # 计算变化
        if previous[1] != 0:  # 使用开盘价
            price_change_percent = ((current[4] - previous[1]) / previous[1]) * 100  # 收盘价与开盘价对比
        else:
            price_change_percent = 0
            
        return {
            'symbol': symbol,
            'current_price': current[4],  # 收盘价
            'previous_price': previous[1],  # 开盘价
            'price_change_percent': price_change_percent,
            'timestamp': current[0]
        }
    except Exception as e:
        # print(f"获取{symbol}历史持仓量数据时出错: {str(e)}")
        return None

def fetch_historical_data_batch(exchange, symbols, timeframe='4h', limit=2, max_workers=30):
    """并发获取多个交易对的历史数据 - 简化后的兼容函数
    
    Args:
        exchange: CCXT交易所实例
        symbols: 交易对符号列表
        timeframe: 时间周期
        limit: 获取数量
        max_workers: 最大线程数
        
    Returns:
        dict: 空字典，因为所有数据已在fetch_market_data_batch中获取
    """
    print("注意: 历史数据已在市场数据获取中一并处理，此函数调用不再需要")
    return {}

def combine_market_data(current_data, historical_data):
    """合并当前市场数据和历史数据
    
    Args:
        current_data: 当前市场数据列表
        historical_data: 历史市场数据字典
        
    Returns:
        list: 合并后的市场数据列表
    """
    # 由于fetch_market_data已经获取了所有需要的数据，这里直接返回current_data
    return current_data

def verify_funding_rates(exchange, symbols, sample_size=10):
    """验证获取到的资金费率数据与Bybit官方报价的准确性（仅用于调试）
    
    Args:
        exchange: CCXT交易所实例
        symbols: 交易对符号列表
        sample_size: 抽样检查的交易对数量
        
    Returns:
        bool: 验证是否通过
    """
    # 如果符号列表少于采样数，则使用全部
    if len(symbols) < sample_size:
        sample_symbols = symbols
    else:
        # 随机选择交易对进行验证
        sample_symbols = random.sample(symbols, sample_size)
    
    print(f"\n===== 资金费率验证 (抽样{len(sample_symbols)}个交易对) =====")
    
    success_count = 0
    for symbol in sample_symbols:
        try:
            # 通过多种方式获取资金费率
            rates = []
            
            # 方式1: 直接获取funding_rate
            try:
                funding_data = exchange.fetch_funding_rate(symbol)
                if funding_data and 'fundingRate' in funding_data:
                    rate1 = funding_data['fundingRate'] * 100
                    rates.append(('API直接获取', rate1))
            except Exception:
                pass
                
            # 方式2: 使用ticker获取
            try:
                ticker = exchange.fetch_ticker(symbol)
                if ticker and 'info' in ticker and 'fundingRate' in ticker['info']:
                    rate2 = float(ticker['info']['fundingRate']) * 100
                    rates.append(('Ticker数据', rate2))
            except Exception:
                pass
                
            # 方式3: 使用市场信息获取
            try:
                market = exchange.market(symbol)
                if market and 'info' in market and 'fundingRate' in market['info']:
                    rate3 = float(market['info']['fundingRate']) * 100
                    rates.append(('市场信息', rate3))
            except Exception:
                pass
            
            # 打印结果
            if rates:
                print(f"\n{symbol} 资金费率比较:")
                for method, rate in rates:
                    print(f"  - {method}: {rate:.6f}%")
                
                # 判断是否一致
                if len(rates) > 1:
                    values = [r[1] for r in rates]
                    max_diff = max(values) - min(values)
                    if max_diff < 0.0001:  # 允许微小误差
                        print(f"  结果: 一致 ✓")
                        success_count += 1
                    else:
                        print(f"  结果: 不一致 ✗ (最大差异: {max_diff:.6f}%)")
                else:
                    print(f"  结果: 只有一种方法成功，无法比较")
                    success_count += 1  # 计为成功，因为没有证据表明不一致
            else:
                print(f"{symbol}: 未能获取资金费率数据")
        
        except Exception as e:
            print(f"{symbol} 验证资金费率时出错: {str(e)}")
    
    # 打印总结果
    if success_count == len(sample_symbols):
        print(f"\n所有抽样交易对的资金费率数据一致或无可比较数据")
        return True
    else:
        print(f"\n{success_count}/{len(sample_symbols)}个交易对的资金费率数据一致")
        return False 