import ccxt
import threading
import os

def print_banner():
    """显示应用程序横幅"""
    print("=" * 60)
    print(" " * 20 + "价格监控系统" + " " * 20)
    print("=" * 60)
    print(" * 支持多种策略")
    print(" * 可以同时运行多个策略")
    print(" * 自动检测交易对变化")
    print("=" * 60)

def main():
    """主函数，用于启动应用程序"""
    print_banner()
    print('CCXT 版本:', ccxt.__version__)
    
    try:
        # 确保必要的目录存在
        os.makedirs("market_data", exist_ok=True)
        
        # 询问用户要运行哪个策略
        print("请选择要运行的策略:")
        print("1. 价格异动策略")
        print("2. 永续合约市场数据策略")
        print("0. 同时运行所有策略")
        
        choice = input("请输入策略编号: ")
        
        if choice == '1':
            # 运行价格异动策略
            from price_volatility_strategy import PriceVolatilityStrategy
            strategy = PriceVolatilityStrategy()
            strategy.initialize()
            strategy.execute()
        elif choice == '2':
            # 导入并运行永续合约市场数据策略
            from market_data_strategy import MarketDataStrategy
            strategy = MarketDataStrategy()
            strategy.initialize()
            strategy.execute()
        elif choice == '0':
            # 导入相关模块
            from price_volatility_strategy import PriceVolatilityStrategy
            from market_data_strategy import MarketDataStrategy
            
            # 创建策略实例
            strategies = [
                PriceVolatilityStrategy(),
                MarketDataStrategy()
            ]
            
            # 初始化策略
            print("正在初始化所有策略...")
            for strategy in strategies:
                strategy.initialize()
            
            # 创建线程运行策略
            threads = [
                threading.Thread(target=strategy.execute)
                for strategy in strategies
            ]
            
            # 启动所有线程
            for thread in threads:
                thread.start()
                
            print("所有策略已启动!")
            
            # 等待键盘中断信号
            try:
                # 主线程等待
                for thread in threads:
                    thread.join()
            except KeyboardInterrupt:
                print("\n正在停止所有策略...")
                for strategy in strategies:
                    strategy.stop()
                print("所有策略已停止")
        else:
            print("无效的选择，程序退出")
            
    except KeyboardInterrupt:
        print('\n正在停止策略...')
        if 'strategy' in locals():
            strategy.stop()
        elif 'strategies' in locals():
            for strategy in strategies:
                strategy.stop()
        print('策略已停止')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n程序已停止运行')
