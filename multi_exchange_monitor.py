#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import ccxt.pro as ccxtpro
import os
import sys
import signal
from tabulate import tabulate
import time
import argparse

# 防止Python 3.8中的事件循环关闭警告
if sys.platform.startswith('win'):
    # Windows系统特定修复
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 设置代理环境变量
os.environ['HTTP_PROXY'] = 'socks5://127.0.0.1:10808'
os.environ['HTTPS_PROXY'] = 'socks5://127.0.0.1:10808'
os.environ['ALL_PROXY'] = 'socks5://127.0.0.1:10808'

# 全局变量
should_exit = False
exchanges = {}  # 保存所有交易所实例
all_symbols = {}  # 保存所有交易对: {symbol: [交易所列表]}
consolidated_symbols = []  # 整合后的交易对列表
tickers_data = {}  # 存储所有ticker数据: {symbol: {exchange: ticker}}
sort_option = 'price'  # 默认排序选项
market_type = 'perpetual'  # 默认监控永续合约，可选: 'spot', 'perpetual', 'both'
args = None  # 命令行参数

# 存储每个交易所的原始交易对格式: {exchange_id: {normalized_symbol: original_symbol}}
exchange_symbol_maps = {}

# 错误计数器和最大错误次数
error_counters = {}  # 格式: {"exchange:symbol": count}
MAX_ERROR_COUNT = 3  # 最大尝试次数

# 在全局变量区域添加
last_display_time = 0  # 上次显示时间戳

# 添加全局变量用于分页
# 在已有全局变量下面添加
current_page = 1  # 当前页码
per_page = 50  # 每页显示数量
auto_scroll = False  # 是否自动滚动

# 添加市值全局变量和统计信息变量
market_caps = {}  # 存储市值信息: {symbol: market_cap}
exchange_stats = {
    'bybit': {'spot': 0, 'perpetual': 0},
    'binance': {'spot': 0, 'perpetual': 0},
    'okx': {'spot': 0, 'perpetual': 0},
}

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description='多交易所价格监控工具')
    parser.add_argument('--sort', '-s', choices=['price', 'volume', 'market_cap'], default='market_cap',
                        help='排序方式: 按价格(price)、交易量(volume)或市值(market_cap)')
    parser.add_argument('--proxy', '-p', default='127.0.0.1:10808',
                        help='SOCKS5代理地址，格式为host:port')
    parser.add_argument('--market', '-m', choices=['spot', 'perpetual', 'both'], default='perpetual',
                        help='市场类型: 现货(spot)、永续合约(perpetual)或两者(both)')
    parser.add_argument('--limit', '-l', type=int, default=0,
                        help='显示的交易对总数，默认为0(显示全部)')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='启用调试模式，显示更多错误信息')
    parser.add_argument('--batch-size', '-b', type=int, default=50,
                        help='批量处理交易对的数量，较小的值可能更稳定但更慢，较大的值更快但可能不稳定')
    parser.add_argument('--no-proxy', '-n', action='store_true',
                        help='不使用代理，直接连接交易所（在某些网络环境下可能更快）')
    parser.add_argument('--timeout', '-t', type=int, default=30000,
                        help='交易所API超时时间（毫秒）')
    parser.add_argument('--refresh', '-r', type=float, default=2.0,
                        help='屏幕刷新间隔（秒），较大的值可减少闪烁')
    parser.add_argument('--no-clear', '-c', action='store_true',
                        help='不清屏直接更新，可减少闪烁但可能导致输出混乱')
    parser.add_argument('--per-page', '-pp', type=int, default=50,
                        help='每页显示的交易对数量')
    parser.add_argument('--auto-scroll', '-a', action='store_true',
                        help='启用自动滚动模式，定时切换页面')
    parser.add_argument('--scroll-interval', '-si', type=float, default=10.0,
                        help='自动滚动间隔（秒）')
    return parser.parse_args()

# 设置信号处理程序用于优雅退出
def signal_handler(sig, frame):
    global should_exit
    print("\n收到退出信号，正在关闭连接...")
    should_exit = True
    # 确保程序能及时退出
    sys.exit(0)

# 注册信号处理程序
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def create_exchange_config(proxy_address):
    """创建交易所配置"""
    host, port = proxy_address.split(':')
    
    return {
        'newUpdates': True,
        'enableRateLimit': True,
        'timeout': 60000,  # 1分钟
        'proxies': {
            'http': f'socks5://{proxy_address}',
            'https': f'socks5://{proxy_address}',
        },
        'options': {
            'ws': {
                'options': {
                    'proxy': {
                        'host': host,
                        'port': int(port),
                        'protocol': 'socks5',
                    }
                }
            }
        }
    }

async def setup_exchange(exchange_id, proxy_address):
    """设置交易所连接"""
    print(f"正在连接 {exchange_id.upper()} 的WebSocket API...")
    
    # 创建配置
    if args.no_proxy:
        config = {
            'newUpdates': True,
            'enableRateLimit': True,
            'timeout': args.timeout
        }
        print(f"不使用代理直接连接 {exchange_id.upper()}")
    else:
        config = create_exchange_config(proxy_address)
        config['timeout'] = args.timeout
    
    # 创建aiohttp session
    try:
        import aiohttp
        
        # 如果使用代理
        if not args.no_proxy:
            try:
                from aiohttp_socks import ProxyConnector
                connector = ProxyConnector.from_url(f'socks5://{proxy_address}')
                session = aiohttp.ClientSession(connector=connector)
                config['session'] = session
                print(f"已为 {exchange_id} 配置SOCKS5代理 ({proxy_address})")
            except ImportError:
                print(f"警告: 未安装aiohttp_socks库，WebSocket可能无法通过代理连接")
                print("请运行: pip install aiohttp-socks")
                session = None
            except Exception as e:
                print(f"设置 {exchange_id} 代理连接器时出错: {e}")
                session = None
        else:
            # 不使用代理，使用标准连接器
            connector = aiohttp.TCPConnector(limit=100)  # 增加连接数上限
            session = aiohttp.ClientSession(connector=connector)
            config['session'] = session
            print(f"为 {exchange_id} 创建了标准连接 (不使用代理)")
            
    except Exception as e:
        print(f"设置 {exchange_id} 会话时出错: {e}")
        session = None
    
    # 创建交易所实例
    try:
        exchange_class = getattr(ccxtpro, exchange_id)
        exchange = exchange_class(config)
        
        # 存储到全局变量
        exchanges[exchange_id] = {
            'instance': exchange,
            'session': session
        }
        
        return exchange
    except Exception as e:
        print(f"创建 {exchange_id} 交易所实例失败: {e}")
        return None

async def get_exchange_symbols(exchange_id):
    """获取交易所的所有交易对"""
    global market_type, exchange_stats
    
    exchange = exchanges[exchange_id]['instance']
    
    try:
        await exchange.load_markets()
        print(f"{exchange_id.upper()} 市场数据加载成功，共有 {len(exchange.markets)} 个交易对")
        
        # 存储交易对
        symbols = []
        original_symbols = {}  # 存储原始交易对格式
        
        # 计数器
        spot_count = 0
        perpetual_count = 0
        
        # 不同交易所的合约标识不同
        for symbol in exchange.symbols:
            market = exchange.markets[symbol]
            is_spot = False
            is_perpetual = False
            
            # 检查是否为现货交易对 (通常不含:且以USDT结尾)
            if '/USDT' in symbol and not ':' in symbol and market.get('spot', False):
                is_spot = True
                spot_count += 1
            
            # 检查是否为永续合约
            # 币安的永续合约格式通常是 BTC/USDT:USDT
            if exchange_id == 'binance' and ':USDT' in symbol and symbol.endswith(':USDT'):
                is_perpetual = True
                perpetual_count += 1
            
            # OKX的永续合约格式通常也是 BTC/USDT:USDT
            elif exchange_id == 'okx' and ':USDT' in symbol and symbol.endswith(':USDT'):
                is_perpetual = True
                perpetual_count += 1
            
            # Bybit的永续合约格式通常是 BTC/USDT 或 BTC/USDT:USDT
            elif exchange_id == 'bybit' and market.get('linear', False) and market.get('swap', False):
                if symbol.endswith('/USDT') or (symbol.endswith(':USDT') and '/USDT:' in symbol):
                    is_perpetual = True
                    perpetual_count += 1
            
            # 根据市场类型选择添加对应的交易对
            should_add = False
            if market_type == 'spot' and is_spot:
                should_add = True
            elif market_type == 'perpetual' and is_perpetual:
                should_add = True
            elif market_type == 'both' and (is_spot or is_perpetual):
                should_add = True
                
            # 如果符合条件，添加到列表
            if should_add:
                # 存储原始交易对格式
                original_symbol = symbol
                
                # 确保符号格式一致性，用于后续比较
                normalized_symbol = normalize_symbol(symbol, exchange_id, market)
                if normalized_symbol:
                    symbols.append(normalized_symbol)
                    # 保存原始格式和标准化格式的映射关系
                    original_symbols[normalized_symbol] = original_symbol
        
        # 更新交易所统计信息
        if exchange_id in exchange_stats:
            exchange_stats[exchange_id]['spot'] = spot_count
            exchange_stats[exchange_id]['perpetual'] = perpetual_count
        
        print(f"{exchange_id.upper()} 交易对统计: 现货 {spot_count} 个, 永续合约 {perpetual_count} 个")
        print(f"{exchange_id.upper()} 已选择的交易对: {len(symbols)} 个")
        
        # 保存原始格式映射
        if exchange_id not in exchange_symbol_maps:
            exchange_symbol_maps[exchange_id] = {}
        exchange_symbol_maps[exchange_id].update(original_symbols)
        
        return symbols
    
    except Exception as e:
        print(f"获取 {exchange_id} 交易对时出错: {e}")
        import traceback
        traceback.print_exc()
        return []

def normalize_symbol(symbol, exchange_id, market=None):
    """标准化不同交易所的交易对格式"""
    try:
        # 已经是标准格式的不需要处理
        if '/USDT:USDT' in symbol:
            return symbol
        
        # 现货交易对标准化
        if market and market.get('spot', False) and symbol.endswith('/USDT'):
            return symbol  # 保持现货格式不变
        
        # Bybit合约特殊处理 - 如果是BTC/USDT格式，转为BTC/USDT:USDT格式
        if exchange_id == 'bybit' and symbol.endswith('/USDT') and ':' not in symbol:
            # 检查是否为永续合约
            if market and (market.get('linear', False) or market.get('swap', False)):
                base = symbol.split('/')[0]
                return f"{base}/USDT:USDT"
        
        # 其他情况，返回原格式
        return symbol
    except Exception:
        return None

async def consolidate_symbols():
    """整合各交易所的交易对，以bybit为基准"""
    global all_symbols, consolidated_symbols, market_type
    
    print(f"开始整合各交易所{market_type_description(market_type)}交易对...")
    
    # 用于调试的计数器
    stats = {
        'bybit': 0,
        'binance': 0,
        'okx': 0,
        'unique_others': 0,
        'common': 0,
        'total': 0
    }
    
    # 临时存储各交易所交易对
    exchange_symbols = {}
    
    # 清理之前的数据
    all_symbols = {}
    consolidated_symbols = []
    
    # 首先获取所有交易所的交易对
    for exchange_id in exchanges:
        exchange_symbols[exchange_id] = await get_exchange_symbols(exchange_id)
        
        # 更新统计信息
        if exchange_id in stats:
            stats[exchange_id] = len(exchange_symbols[exchange_id])
    
    # 创建一个所有交易对的集合
    all_symbol_set = set()
    for exchange_id, symbols in exchange_symbols.items():
        all_symbol_set.update(symbols)
    
    # 计算交易所之间的共同交易对
    common_symbols = set()
    if 'bybit' in exchange_symbols and 'binance' in exchange_symbols:
        bybit_set = set(exchange_symbols['bybit'])
        binance_set = set(exchange_symbols['binance'])
        common_symbols = bybit_set.intersection(binance_set)
        stats['common'] = len(common_symbols)
    
    # 整合交易对
    for symbol in all_symbol_set:
        # 确定哪些交易所支持此交易对
        supporting_exchanges = []
        for exchange_id, symbols in exchange_symbols.items():
            if symbol in symbols:
                supporting_exchanges.append(exchange_id)
        
        # 更新all_symbols
        all_symbols[symbol] = supporting_exchanges
    
    # 计算各交易所独有的交易对数量
    if 'bybit' in exchange_symbols:
        bybit_set = set(exchange_symbols['bybit'])
        others_set = set()
        for exchange_id, symbols in exchange_symbols.items():
            if exchange_id != 'bybit':
                others_set.update(symbols)
        
        unique_others = others_set - bybit_set
        stats['unique_others'] = len(unique_others)
    
    # 整合后的交易对列表 - 将所有找到的交易对添加到最终列表
    consolidated_symbols = sorted(list(all_symbol_set))
    stats['total'] = len(consolidated_symbols)
    
    # 打印统计信息
    print(f"\n整合结果统计 ({market_type_description(market_type)}):")
    for exchange_id in exchanges:
        if exchange_id in stats:
            print(f"{exchange_id.upper()} 交易对: {stats[exchange_id]}")
    
    if 'common' in stats and stats['common'] > 0:
        print(f"共同交易对: {stats['common']}")
    print(f"其他交易所独有交易对: {stats['unique_others']}")
    print(f"整合后共有 {stats['total']} 个唯一交易对")
    
    # 打印每个交易对由哪些交易所提供
    if consolidated_symbols:
        print("\n样本交易对:")
        for symbol in consolidated_symbols[:5]:  # 只打印前5个作为示例
            exchanges_list = ', '.join(all_symbols.get(symbol, []))
            print(f"{symbol}: 由 {exchanges_list} 提供")
    
        if len(consolidated_symbols) > 5:
            print(f"... 还有 {len(consolidated_symbols) - 5} 个交易对")
    else:
        print("警告: 未找到任何交易对!")
    
    return consolidated_symbols

async def watch_ticker_task(exchange_id, symbol):
    """监控特定交易所特定交易对的价格"""
    global error_counters
    
    exchange = exchanges[exchange_id]['instance']
    
    # 使用交易所特定的符号格式
    if exchange_id in exchange_symbol_maps and symbol in exchange_symbol_maps[exchange_id]:
        # 使用原始交易对格式
        exchange_specific_symbol = exchange_symbol_maps[exchange_id][symbol]
    else:
        # 尝试转换格式
        exchange_specific_symbol = convert_to_exchange_format(symbol, exchange_id)
    
    # 检查是否已经错误太多次
    error_key = f"{exchange_id}:{symbol}"
    if error_key in error_counters and error_counters[error_key] >= MAX_ERROR_COUNT:
        # 如果错误次数太多，跳过此交易对
        return None
    
    try:
        # 尝试获取ticker
        ticker = await exchange.watch_ticker(exchange_specific_symbol)
        
        # 如果成功，重置错误计数
        if error_key in error_counters:
            error_counters[error_key] = 0
        
        # 如果成功，更新数据
        if symbol not in tickers_data:
            tickers_data[symbol] = {}
        
        tickers_data[symbol][exchange_id] = {
            'last': ticker.get('last'),
            'bid': ticker.get('bid'),
            'ask': ticker.get('ask'),
            'volume': ticker.get('volume'),  # 增加交易量信息
            'timestamp': exchange.iso8601(exchange.milliseconds())
        }
        
        return ticker
    except Exception as e:
        # 增加错误计数
        if error_key not in error_counters:
            error_counters[error_key] = 0
        error_counters[error_key] += 1
        
        # 记录错误但不中断程序
        error_msg = str(e)
        # 只打印非连接错误，避免刷屏
        if not ('connection' in error_msg.lower() or 'timeout' in error_msg.lower()):
            # 只在前几次错误时打印错误信息
            if error_counters[error_key] <= 2:  # 只打印前两次错误
                print(f"{exchange_id} 监控 {symbol} 时出错: {error_msg}")
                print(f"尝试使用的交易对格式: {exchange_specific_symbol}")
            elif error_counters[error_key] == MAX_ERROR_COUNT:
                print(f"已停止尝试 {exchange_id} 的 {symbol} (错误次数过多)")
        
        # 检查是否需要从列表中移除此交易对
        if 'not found' in error_msg.lower() or 'does not exist' in error_msg.lower():
            # 从交易对列表中移除
            if symbol in all_symbols and exchange_id in all_symbols[symbol]:
                all_symbols[symbol].remove(exchange_id)
                print(f"已从 {exchange_id} 移除无效交易对: {symbol}")
                
                # 如果没有交易所支持此交易对，从整合列表中移除
                if not all_symbols[symbol]:
                    if symbol in consolidated_symbols:
                        consolidated_symbols.remove(symbol)
                    print(f"交易对 {symbol} 已从监控列表中移除")
        
        # 避免频繁重试无效的请求
        await asyncio.sleep(10)  # 出错后等待更长时间
        return None

def convert_to_exchange_format(standard_symbol, exchange_id):
    """将标准化的符号格式转换为交易所特定的格式"""
    try:
        if exchange_id == 'bybit':
            # 对于bybit，将BTC/USDT:USDT转回BTC/USDT
            if '/USDT:USDT' in standard_symbol:
                base = standard_symbol.split('/')[0]
                return f"{base}/USDT"
        
        # 其他交易所可能需要不同的转换规则
        # 对于binance和okx，标准格式通常已经是它们的原始格式
        
        # 如果没有特殊规则，返回原始符号
        return standard_symbol
    except Exception as e:
        print(f"转换符号格式时出错: {e}")
        return standard_symbol

async def fetch_market_caps():
    """获取市值信息，用于排序"""
    global market_caps
    
    try:
        # 在这里可以添加实际获取市值的代码，例如通过CoinGecko或CoinMarketCap API
        # 为了简单起见，我们这里使用一个基于价格的估算值
        for symbol in consolidated_symbols:
            ticker_info = tickers_data.get(symbol, {})
            if not ticker_info:
                continue
                
            data = get_preferred_ticker_data(symbol, ticker_info)
            if not data or 'last' not in data:
                continue
                
            price = data.get('last', 0)
            volume = data.get('volume', 0) or 0
            
            # 使用价格和交易量的组合作为市值的估计
            # 实际应用中应当使用真实市值数据替换
            market_cap = price * (volume or 1) 
            
            # 对某些重要币种赋予更高权重
            base_currency = symbol.split('/')[0] if '/' in symbol else symbol
            if base_currency == 'BTC':
                market_cap *= 10  # 比特币权重提高
            elif base_currency == 'ETH':
                market_cap *= 5   # 以太坊权重提高
            elif base_currency in ['BNB', 'SOL', 'XRP', 'ADA', 'DOGE']:
                market_cap *= 2   # 其他主要币种权重提高
                
            market_caps[symbol] = market_cap
            
    except Exception as e:
        print(f"获取市值信息时出错: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

def get_market_cap_for_sorting(symbol):
    """获取用于排序的市值"""
    try:
        return market_caps.get(symbol, 0)
    except Exception:
        return 0

async def watch_all_tickers():
    """监控所有整合后的交易对价格，采用批量处理方式提高性能"""
    global should_exit, args, last_display_time, current_page, auto_scroll
    
    total_symbols = len(consolidated_symbols)
    if total_symbols == 0:
        print("错误: 没有找到任何交易对可以监控")
        return
        
    print(f"开始监控所有交易对价格 (共 {total_symbols} 个)...")
    
    # 创建一个退出事件
    exit_event = asyncio.Event()
    
    # 批处理大小
    batch_size = args.batch_size
    print(f"使用批处理大小: {batch_size} (可通过 --batch-size 参数调整)")
    print(f"屏幕刷新间隔: {args.refresh}秒 (可通过 --refresh 参数调整)")
    
    # 使用命令行参数设置每页条数和自动滚动
    global per_page
    per_page = args.per_page
    auto_scroll = args.auto_scroll
    print(f"每页显示: {per_page} 个交易对 (可通过 --per-page 参数调整)")
    if auto_scroll:
        print(f"自动滚动: 开启, 每 {args.scroll_interval} 秒切换一次页面")
    
    # 上次自动滚动时间
    last_scroll_time = time.time()
    
    # 定义一个任务完成回调
    def task_done_callback(task):
        try:
            task.result()  # 获取结果，捕获任何异常
        except asyncio.CancelledError:
            pass  # 忽略取消异常
        except Exception as e:
            if args and args.debug:
                print(f"任务执行出错: {e}")
    
    # 监控循环    
    while not should_exit:
        # 控制刷新频率 - 判断是否应该刷新屏幕
        current_time = time.time()
        
        # 更新市值数据
        await fetch_market_caps()
        
        # 检查是否应该自动翻页
        if auto_scroll and current_time - last_scroll_time >= args.scroll_interval:
            # 计算总页数
            total_pages = (len(tickers_data) + per_page - 1) // per_page
            if total_pages > 0:
                current_page = (current_page % total_pages) + 1
                last_scroll_time = current_time
        
        # 检查是否应该刷新屏幕
        if current_time - last_display_time >= args.refresh:
            display_tickers()
            last_display_time = current_time
            
            # 检查用户输入（非阻塞方式）
            await check_user_input()
        
        # 将交易对列表分成多个批次
        batches = [consolidated_symbols[i:i + batch_size] for i in range(0, len(consolidated_symbols), batch_size)]
        
        for batch_idx, batch_symbols in enumerate(batches):
            if should_exit:
                break
                
            tasks = []
            try:
                # 为每个批次创建任务
                if args.debug:
                    print(f"处理批次 {batch_idx+1}/{len(batches)} ({len(batch_symbols)} 个交易对)")
                
                # 为批次中的交易对创建任务
                for symbol in batch_symbols:
                    for exchange_id in all_symbols.get(symbol, []):
                        error_key = f"{exchange_id}:{symbol}"
                        # 跳过错误次数过多的交易对
                        if error_key in error_counters and error_counters[error_key] >= MAX_ERROR_COUNT:
                            continue
                            
                        task = asyncio.create_task(watch_ticker_task(exchange_id, symbol))
                        task.add_done_callback(task_done_callback)
                        tasks.append(task)
                
                # 等待批次任务完成或退出信号
                if tasks:
                    # 创建一个不会立即完成的任务，用于监听退出事件
                    exit_task = asyncio.create_task(exit_event.wait())
                    
                    # 将任务列表加入等待事件
                    pending = set(tasks + [exit_task])
                    
                    # 等待任务完成或退出事件
                    done, pending = await asyncio.wait(
                        pending, 
                        timeout=min(args.refresh / 2, 1.0),  # 减少超时时间但不低于刷新时间的一半
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    # 检查是否应该退出
                    if should_exit or exit_task in done:
                        # 取消所有未完成的任务
                        for task in pending:
                            task.cancel()
                        break
                
                # 短暂等待后继续下一批
                await asyncio.sleep(0.1)
                
            except asyncio.CancelledError:
                break  # 任务被取消，退出循环
            except Exception as e:
                print(f"批处理循环出错: {e}")
                if args.debug:
                    import traceback
                    traceback.print_exc()
                await asyncio.sleep(2)  # 出错后等待更长时间再重试
    
    # 退出前确保清理
    print("正在清理监控任务...")
    
    # 确保所有任务被取消
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            task.cancel()
            
    # 设置退出事件，通知所有等待的任务
    exit_event.set()

async def check_user_input():
    """非阻塞方式检查用户输入"""
    if sys.platform.startswith('win'):
        # Windows下的实现 - 使用msvcrt
        try:
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                handle_user_input(key)
        except Exception:
            pass
    else:
        # Unix/Linux/Mac下的实现 - 更复杂，这里仅作示意
        # 实际应用中可能需要更复杂的终端控制
        try:
            import select
            # 非阻塞方式检查stdin
            r, _, _ = select.select([sys.stdin], [], [], 0)
            if r:
                key = sys.stdin.read(1).lower()
                handle_user_input(key)
        except Exception:
            pass

def handle_user_input(key):
    """处理用户输入的按键"""
    global current_page, auto_scroll, should_exit
    
    if key == 'n':  # 下一页
        # 计算总页数
        total_pages = (len(tickers_data) + per_page - 1) // per_page
        if total_pages > 0:
            current_page = min(current_page + 1, total_pages)
    elif key == 'p':  # 上一页
        current_page = max(current_page - 1, 1)
    elif key == 'a':  # 切换自动滚动
        auto_scroll = not auto_scroll
        print(f"自动滚动: {'开启' if auto_scroll else '关闭'}")
    elif key == 'q':  # 退出
        should_exit = True
        print("用户请求退出...")

def display_tickers():
    """展示价格数据，带分页和导航栏"""
    global args, current_page, per_page, auto_scroll  # 确保引用全局变量
    
    # 如果设置了清屏，则执行清屏
    if not args.debug and not args.no_clear:
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
    
    # 准备表格数据
    table_data = []
    
    # 检查是否有有效的数据可以显示
    if not tickers_data:
        print("正在获取数据，请稍候...")
        return
    
    # 使用全局排序选项
    global sort_option
    
    # 有效的数据数量
    valid_data_count = len([s for s in tickers_data.keys() if any(tickers_data[s].values())])
    
    # 显示错误计数
    error_symbol_count = len(error_counters)
    active_error_count = len([k for k, v in error_counters.items() if v >= MAX_ERROR_COUNT])
    
    # 根据不同排序选项排列
    try:
        if sort_option == 'price':
            # 按价格从高到低排序
            sorted_symbols = sorted(
                tickers_data.keys(),
                key=lambda s: get_price_for_sorting(s),
                reverse=True
            )
        elif sort_option == 'volume':
            # 按交易量从高到低排序
            sorted_symbols = sorted(
                tickers_data.keys(),
                key=lambda s: get_volume_for_sorting(s),
                reverse=True
            )
        elif sort_option == 'market_cap':
            # 按市值从高到低排序
            sorted_symbols = sorted(
                tickers_data.keys(),
                key=lambda s: get_market_cap_for_sorting(s),
                reverse=True
            )
        else:
            # 默认按市值排序
            sorted_symbols = sorted(
                tickers_data.keys(),
                key=lambda s: get_market_cap_for_sorting(s),
                reverse=True
            )
    except Exception as e:
        # 如果排序出错，使用未排序的列表
        print(f"排序时出错: {e}")
        sorted_symbols = list(tickers_data.keys())
    
    # 计算总页数
    total_pages = (len(sorted_symbols) + per_page - 1) // per_page
    
    # 确保current_page在有效范围内
    if total_pages > 0:
        current_page = max(1, min(current_page, total_pages))
    else:
        current_page = 1
    
    # 计算当前页的起始和结束索引
    start_idx = (current_page - 1) * per_page
    end_idx = min(start_idx + per_page, len(sorted_symbols))
    
    # 处理显示数据
    for idx, symbol in enumerate(sorted_symbols[start_idx:end_idx], start=start_idx+1):
        try:
            ticker_info = tickers_data.get(symbol, {})
            
            if not ticker_info:
                continue
            
            # 获取价格数据，优先使用bybit
            data = get_preferred_ticker_data(symbol, ticker_info)
            if not data or 'last' not in data or data['last'] is None:
                continue  # 跳过没有完整数据的交易对
            
            # 所有提供该交易对的交易所
            exchanges_list = all_symbols.get(symbol, [])
            exchanges_str = ', '.join(exchanges_list)
            
            # 获取主要数据来源交易所
            primary_exchange = "bybit" if "bybit" in ticker_info else next(iter(ticker_info.keys()))
            
            # 格式化价格显示（高价格币种显示整数，低价格币种显示更多小数位）
            price_format = '.2f' if data['last'] >= 10 else ('.4f' if data['last'] >= 0.1 else '.8f')
            last_price = f"{data['last']:{price_format}}"
            bid_price = f"{data['bid']:{price_format}}" if data['bid'] else "-"
            ask_price = f"{data['ask']:{price_format}}" if data['ask'] else "-"
            
            # 格式化交易量显示
            volume = data.get('volume')
            volume_str = f"{volume:.2f}" if volume else "-"
            
            # 获取交易对的基础币种
            base_currency = symbol.split('/')[0] if '/' in symbol else symbol
            
            # 获取市值估算（用于排名显示）
            market_cap = market_caps.get(symbol, 0)
            market_cap_display = f"{market_cap:.2f}" if market_cap else "-"
            
            # 添加颜色代码 (可以实现，但在Windows命令行可能不显示，这里仅做示例)
            # price_color = '\033[92m' if last_price > previous_price else '\033[91m'
            
            # 添加序号
            table_data.append([
                idx,                          # 序号（考虑分页）
                base_currency,                # 显示基础货币名称，而不是完整的交易对名称
                last_price,                   # 最新价格
                bid_price,                    # 买入价
                ask_price,                    # 卖出价
                volume_str,                   # 交易量
                primary_exchange.upper(),     # 数据来源
                f"{len(exchanges_list)}家",    # 提供此交易对的交易所数量
            ])
        except Exception as e:
            # 如果处理某个交易对时出错，跳过它
            if args.debug:
                print(f"处理交易对 {symbol} 数据时出错: {e}")
            continue
    
    # 如果是不清屏模式，添加分隔线
    if args.no_clear:
        print("\n" + "-"*80)
    
    # 生成表头和分隔线
    headers = ["序号", "币种", "最新价格", "买入价", "卖出价", "24H交易量", "数据来源", "交易所数"]
    print(f"\n{'='*80}")
    print(f"多交易所实时{market_type_description(market_type)}价格监控 - 更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    # 打印表格
    print(tabulate(table_data, headers=headers, tablefmt="grid", numalign="right"))
    
    # 打印分页信息
    page_info = f"页码: {current_page}/{total_pages}"
    display_info = f"显示: {len(table_data)}/{valid_data_count} 个交易对"
    
    # 计算和显示交易所统计信息
    exchange_info = []
    for exchange_id, stats in exchange_stats.items():
        if exchange_id in exchanges:  # 只显示已连接的交易所
            spot_info = f"{exchange_id.upper()}现货: {stats['spot']}"
            perp_info = f"{exchange_id.upper()}合约: {stats['perpetual']}"
            exchange_info.extend([spot_info, perp_info])
    
    exchange_stats_str = "  ".join(exchange_info)
    
    # 打印底部导航栏和统计信息
    print(f"\n{page_info}  {display_info}  排序: {sort_option_description(sort_option)}")
    print(f"{exchange_stats_str}")
    print(f"操作: [P]上一页  [N]下一页  [A]自动滚动({auto_scroll_status()})  [Q]退出")
    print(f"已忽略 {active_error_count}/{error_symbol_count} 个问题交易对")

def auto_scroll_status():
    """返回自动滚动状态描述"""
    return "开启" if auto_scroll else "关闭"

def sort_option_description(option):
    """将排序选项转为中文描述"""
    if option == 'price':
        return "价格"
    elif option == 'volume':
        return "交易量"
    elif option == 'market_cap':
        return "市值"
    return option

def get_preferred_ticker_data(symbol, ticker_info):
    """获取首选的ticker数据，优先使用bybit"""
    # 优先使用bybit
    if 'bybit' in ticker_info:
        return ticker_info['bybit']
    
    # 其次使用binance
    if 'binance' in ticker_info:
        return ticker_info['binance']
    
    # 再次使用okx
    if 'okx' in ticker_info:
        return ticker_info['okx']
    
    # 最后使用任何可用的交易所
    return next(iter(ticker_info.values()))

def get_price_for_sorting(symbol):
    """获取用于排序的价格，优先使用bybit数据"""
    try:
        ticker_info = tickers_data.get(symbol, {})
        if not ticker_info:
            return 0
        
        data = get_preferred_ticker_data(symbol, ticker_info)
        return data['last'] if data and 'last' in data else 0
    except Exception:
        return 0

def get_volume_for_sorting(symbol):
    """获取用于排序的交易量，优先使用bybit数据"""
    try:
        ticker_info = tickers_data.get(symbol, {})
        if not ticker_info:
            return 0
        
        data = get_preferred_ticker_data(symbol, ticker_info)
        return data.get('volume', 0) or 0  # 确保None转为0
    except Exception:
        return 0

async def close_all_exchanges():
    """关闭所有交易所连接"""
    for exchange_id, exchange_data in exchanges.items():
        try:
            if hasattr(exchange_data['instance'], 'close') and callable(exchange_data['instance'].close):
                await exchange_data['instance'].close()
            
            session = exchange_data.get('session')
            if session and not session.closed:
                await session.close()
            
            print(f"{exchange_id} 连接已关闭")
        except Exception as e:
            print(f"关闭 {exchange_id} 资源时出错: {e}")

def market_type_description(market_type):
    """将市场类型转为中文描述"""
    if market_type == 'spot':
        return "现货"
    elif market_type == 'perpetual':
        return "永续合约"
    elif market_type == 'both':
        return "现货和永续合约"
    return market_type

async def main():
    """主函数"""
    global sort_option, market_type, args
    
    try:
        # 解析命令行参数
        args = parse_args()
        sort_option = args.sort
        market_type = args.market
        proxy_address = args.proxy
        
        # 显示欢迎信息
        print("\n" + "="*80)
        print("多交易所加密货币价格监控工具 - 基于CCXT Pro")
        print("="*80)
        print("本工具使用WebSocket API实时监控多个交易所的加密货币价格。")
        print("支持交易所: Binance, OKX, Bybit\n")
        
        # 显示高级选项
        print("高级选项:")
        print(f"  批处理大小: {args.batch_size} (--batch-size)")
        print(f"  每页显示: {args.per_page} (--per-page)")
        print(f"  排序方式: {sort_option_description(args.sort)} (--sort)")
        print(f"  代理状态: {'不使用' if args.no_proxy else '使用'} (--no-proxy)")
        print(f"  刷新间隔: {args.refresh}秒 (--refresh)")
        print(f"  自动滚动: {'开启' if args.auto_scroll else '关闭'} (--auto-scroll)")
        
        # 确保安装了必要的库
        try:
            import aiohttp
            try:
                import aiohttp_socks
            except ImportError:
                print("尝试安装 aiohttp-socks...")
                import pip
                pip.main(['install', 'aiohttp-socks'])
                import aiohttp_socks
                print("aiohttp-socks 安装成功")
            
            try:
                import tabulate
            except ImportError:
                print("尝试安装 tabulate...")
                import pip
                pip.main(['install', 'tabulate'])
                import tabulate
                print("tabulate 安装成功")
                
            try:
                import argparse
            except ImportError:
                print("尝试安装 argparse...")
                import pip
                pip.main(['install', 'argparse'])
                import argparse
                print("argparse 安装成功")
        except Exception as e:
            print(f"库导入/安装失败: {e}")
            print("继续尝试，但可能无法使用代理连接WebSocket")
        
        # 用户选择交易所
        print("\n请选择要监控的交易所（输入数字，多选用逗号分隔）:")
        print("1. 币安 (Binance)")
        print("2. OKX")
        print("3. Bybit")
        
        choice = input("您的选择 [默认全部]: ").strip()
        selected_exchanges = []
        
        if not choice:  # 如果用户没有输入，默认全部
            selected_exchanges = ['binance', 'okx', 'bybit']
        else:
            for c in choice.split(','):
                c = c.strip()
                if c == '1':
                    selected_exchanges.append('binance')
                elif c == '2':
                    selected_exchanges.append('okx')
                elif c == '3':
                    selected_exchanges.append('bybit')
        
        # 确保至少有一个选择
        if not selected_exchanges:
            print("未选择任何交易所，默认选择全部")
            selected_exchanges = ['binance', 'okx', 'bybit']
        
        # 用户选择市场类型
        if market_type == 'both':  # 如果命令行已经选择了both，就不再提示
            print(f"\n已选择市场类型: {market_type_description(market_type)}")
        else:
            print("\n请选择要监控的市场类型:")
            print("1. 现货市场")
            print("2. 永续合约")
            print("3. 两者都监控")
            
            market_choice = input("您的选择 [默认永续合约]: ").strip()
            
            if market_choice == '1':
                market_type = 'spot'
            elif market_choice == '2':
                market_type = 'perpetual'
            elif market_choice == '3':
                market_type = 'both'
            # 如果用户没有输入，使用默认值
        
        print(f"\n已选择交易所: {', '.join([ex.upper() for ex in selected_exchanges])}")
        print(f"已选择市场类型: {market_type_description(market_type)}")
        print(f"排序方式: {sort_option_description(sort_option)}")
        print(f"使用代理: {proxy_address}")
        print(f"调试模式: {'开启' if args.debug else '关闭'}")
        
        # 验证代理配置
        try:
            host, port = proxy_address.split(':')
            port = int(port)
            print(f"代理配置有效: {host}:{port}")
        except Exception as e:
            print(f"警告: 代理配置格式无效 ({e}), 可能导致连接问题")

        print("\n正在初始化交易所连接，这可能需要几分钟时间...\n")
        
        # 初始化所有选定的交易所
        success_count = 0
        for exchange_id in selected_exchanges:
            exchange = await setup_exchange(exchange_id, proxy_address)
            if exchange:
                success_count += 1
                
        if success_count == 0:
            print("\n错误: 所有交易所连接均失败。请检查网络和代理设置。")
            return
            
        print("\n成功连接到 {}/{} 个交易所".format(success_count, len(selected_exchanges)))
        
        # 整合交易对
        await consolidate_symbols()
        
        if not consolidated_symbols:
            print("\n错误: 未找到任何交易对。请检查网络连接和交易所设置。")
            return
            
        print("\n准备开始监控价格数据...")
        print("初始化完成，开始获取实时价格信息...")
        
        # 监控价格
        await watch_all_tickers()
    
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        should_exit = True
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
    finally:
        # 确保关闭所有连接
        print("\n正在关闭所有连接...")
        await close_all_exchanges()
        print("所有连接已关闭")
        
# 运行主函数
if __name__ == "__main__":
    try:
        # 先初始化命令行参数
        args = parse_args()
        
        # 然后运行主函数
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        # 确保退出信号被处理
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"主程序出错: {e}")
        if args and args.debug:
            import traceback
            traceback.print_exc()
    finally:
        print("程序已结束") 