#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import ccxt.pro as ccxtpro
import os
import sys
import signal

# 防止Python 3.8中的事件循环关闭警告
if sys.platform.startswith('win'):
    # Windows系统特定修复
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 设置代理环境变量
os.environ['HTTP_PROXY'] = 'socks5://127.0.0.1:10808'
os.environ['HTTPS_PROXY'] = 'socks5://127.0.0.1:10808'
os.environ['ALL_PROXY'] = 'socks5://127.0.0.1:10808'

# 全局变量用来控制程序是否应该退出
should_exit = False

# 设置信号处理程序用于优雅退出
def signal_handler(sig, frame):
    global should_exit
    print("\n收到退出信号，关闭连接...")
    should_exit = True

# 注册信号处理程序
signal.signal(signal.SIGINT, signal_handler)

async def monitor_btc_price(exchange_id="binance"):
    """通过WebSocket监控BTC价格"""
    print(f"正在连接 {exchange_id.upper()} 的WebSocket API...")
    
    # 创建配置
    config = {
        'newUpdates': True,
        'enableRateLimit': True,
        'timeout': 60000,  # 1分钟
        # 设置代理配置
        'proxies': {
            'http': 'socks5://127.0.0.1:10808',
            'https': 'socks5://127.0.0.1:10808',
        }
    }
    
    session = None
    
    # 在异步上下文中创建aiohttp session和connector
    try:
        # 导入和配置aiohttp_socks
        import aiohttp
        from aiohttp_socks import ProxyConnector
        
        # 在异步函数内创建connector和session
        connector = ProxyConnector.from_url('socks5://127.0.0.1:10808')
        session = aiohttp.ClientSession(connector=connector)
        
        # 将session传递给ccxt交易所实例
        config['session'] = session
        print(f"已配置SOCKS5代理")
    except ImportError:
        print(f"警告: 未安装aiohttp_socks库，WebSocket可能无法通过代理连接")
        print("请运行: pip install aiohttp-socks")
    except Exception as e:
        print(f"设置代理连接器时出错: {e}")
    
    # 设置WebSocket专用代理选项
    config['options'] = {
        'ws': {
            'options': {
                'proxy': {
                    'host': '127.0.0.1',
                    'port': 10808,
                    'protocol': 'socks5',
                }
            }
        }
    }
    
    # 创建交易所实例
    exchange_class = getattr(ccxtpro, exchange_id)
    exchange = exchange_class(config)
    
    symbol = 'BTC/USDT'
    
    try:
        # 加载市场数据
        await exchange.load_markets()
        print(f"市场数据加载成功，开始WebSocket连接...")
        
        # 持续监控价格
        while not should_exit:
            try:
                ticker = await exchange.watch_ticker(symbol)
                
                # 提取并显示价格信息
                timestamp = exchange.iso8601(exchange.milliseconds())
                last_price = ticker['last'] if 'last' in ticker else None
                bid = ticker['bid'] if 'bid' in ticker else None
                ask = ticker['ask'] if 'ask' in ticker else None
                
                # 显示价格信息
                print(f"时间: {timestamp}, {symbol} 价格: {last_price}, 买入: {bid}, 卖出: {ask}")
                
                # 可选的间隔时间
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"数据获取出错: {e}")
                print("5秒后重试...")
                await asyncio.sleep(5)
    except Exception as e:
        print(f"连接过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 确保资源正确关闭
        try:
            if hasattr(exchange, 'close') and callable(exchange.close):
                await exchange.close()
            
            if session and not session.closed:
                await session.close()
            
            print("连接已关闭")
        except Exception as e:
            print(f"关闭资源时出错: {e}")

# 主函数
async def main():
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
    except Exception as e:
        print(f"库导入/安装失败: {e}")
        print("继续尝试，但可能无法使用代理连接WebSocket")
    
    # 监控BTC价格
    await monitor_btc_price()

# 运行主函数
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        print("程序已结束")
