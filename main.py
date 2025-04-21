import ccxt
import asyncio
import threading
import os
import time
import traceback
from datetime import datetime
import multiprocessing

from market_data_strategy import MarketDataStrategy
from price_volatility_strategy import PriceVolatilityStrategy


def print_banner():
    """显示应用程序横幅"""
    print("=" * 60)
    print(" " * 20 + "价格监控系统" + " " * 20)
    print("=" * 60)
    print(" * 支持多种策略")
    print(" * 可以同时运行多个策略")
    print(" * 自动检测交易对变化")
    print(" * 支持WebSocket实时数据")
    print("=" * 60)

def display_banner():
    """显示程序启动横幅"""
    banner = """
██████╗ ██╗   ██╗██████╗ ██╗████████╗    ██████╗  ██████╗ ████████╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██║╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝ ╚████╔╝ ██████╔╝██║   ██║       ██████╔╝██║   ██║   ██║   
██╔══██╗  ╚██╔╝  ██╔══██╗██║   ██║       ██╔══██╗██║   ██║   ██║   
██████╔╝   ██║   ██████╔╝██║   ██║       ██████╔╝╚██████╔╝   ██║   
╚═════╝    ╚═╝   ╚═════╝ ╚═╝   ╚═╝       ╚═════╝  ╚═════╝    ╚═╝                                                               
    """
    print(banner)
    print("Bybit交易机器人 - 启动时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)

def initialize():
    """初始化程序"""
    display_banner()
    
    # 创建必要的目录
    os.makedirs("logs", exist_ok=True)
    os.makedirs("market_data", exist_ok=True)
    
def run_strategy(strategy):
    """在单独的进程中运行策略
    
    Args:
        strategy: 策略实例
    """
    try:
        strategy.initialize()
        strategy.execute()
    except KeyboardInterrupt:
        print(f"策略 {strategy.name} 被用户中断")
    except Exception as e:
        print(f"策略 {strategy.name} 发生错误: {str(e)}")
        traceback.print_exc()
    finally:
        if hasattr(strategy, 'stop'):
            strategy.stop()

async def run_ws_strategy(strategy):
    """在异步模式下运行WebSocket策略
    
    Args:
        strategy: WebSocket策略实例
    """
    try:
        await strategy.initialize()
        await strategy.execute()
    except KeyboardInterrupt:
        print(f"策略 {strategy.name} 被用户中断")
    except Exception as e:
        print(f"策略 {strategy.name} 发生错误: {str(e)}")
        traceback.print_exc()
    finally:
        if hasattr(strategy, 'stop'):
            if asyncio.iscoroutinefunction(strategy.stop):
                await strategy.stop()
            else:
                strategy.stop()

def run_ws_strategy_wrapper():
    """WebSocket策略的启动包装器，用于在新进程中运行"""
    asyncio.run(run_ws_strategy(MarketDataWsStrategy()))

def main():
    """主函数，用于启动应用程序"""
    initialize()
    
    while True:
        print("\n请选择要运行的策略:")
        print("1. 市场数据策略 (REST API)")
        print("2. 价格波动策略")
        print("3. 运行所有策略")
        print("0. 退出")
        
        choice = input("\n请输入选项编号: ")
        
        if choice == '0':
            print("退出程序")
            break
            
        if choice == '1':
            # 运行市场数据策略
            strategy = MarketDataStrategy()
            run_strategy(strategy)
            
        elif choice == '2':
            # 运行价格波动策略
            strategy = PriceVolatilityStrategy()
            run_strategy(strategy)
            
                
        elif choice == '3':
            # 运行所有策略
            processes = []
            
            # 市场数据策略
            market_data_process = multiprocessing.Process(
                target=run_strategy, 
                args=(MarketDataStrategy(),)
            )
            processes.append(market_data_process)
            
            # 价格波动策略
            volatility_process = multiprocessing.Process(
                target=run_strategy, 
                args=(PriceVolatilityStrategy(),)
            )
            processes.append(volatility_process)
            
            # 市场数据WebSocket策略
            ws_process = multiprocessing.Process(
                target=run_ws_strategy_wrapper
            )
            processes.append(ws_process)
            
            # 启动所有进程
            for process in processes:
                process.start()
            
            try:
                # 等待所有进程完成
                for process in processes:
                    process.join()
            except KeyboardInterrupt:
                print("\n收到中断信号，正在停止所有策略...")
                for process in processes:
                    if process.is_alive():
                        process.terminate()
                
                # 等待所有进程结束
                for process in processes:
                    process.join()
                
        else:
            print("无效的选项，请重新选择")
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n程序已停止运行')
