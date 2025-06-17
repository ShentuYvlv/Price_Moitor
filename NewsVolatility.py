#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻事件价格波动分析工具
分析特定时间点前后X分钟内，各币种价格的波动情况
用于评估新闻事件对加密货币价格的影响

作者: Price Monitor System
创建时间: 2025-06-15
"""

import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Tuple, Optional
import argparse
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 添加父目录到路径，以便导入utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import get_socks5_proxy, get_perpetual_symbols, get_bybit_perpetual_symbols


class NewsVolatilityAnalyzer:
    """新闻事件价格波动分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.exchanges = {}
        self.proxy_config = get_socks5_proxy()
        self.init_exchanges()
        
    def init_exchanges(self):
        """初始化交易所连接"""
        print("正在初始化交易所连接...")

        # 初始化币安
        try:
            self.exchanges['binance'] = ccxt.binance({
                'apiKey': '',
                'secret': '',
                'timeout': 30000,
                'enableRateLimit': True,
                'proxies': self.proxy_config,
                'options': {
                    'defaultType': 'spot'  # 默认现货，后续可切换
                }
            })
            print("✅ Binance 连接成功")
        except Exception as e:
            print(f"❌ Binance 连接失败: {e}")

        # 初始化Bybit
        try:
            self.exchanges['bybit'] = ccxt.bybit({
                'apiKey': '',
                'secret': '',
                'timeout': 30000,
                'enableRateLimit': True,
                'proxies': self.proxy_config,
                'options': {
                    'defaultType': 'spot'
                }
            })
            print("✅ Bybit 连接成功")
        except Exception as e:
            print(f"❌ Bybit 连接失败: {e}")
    
    def convert_time_to_timestamp(self, time_str: str) -> int:
        """将时间字符串转换为时间戳"""
        try:
            # 支持多种时间格式
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d %H:%M'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(time_str, fmt)
                    return int(dt.timestamp() * 1000)
                except ValueError:
                    continue
                    
            raise ValueError(f"无法解析时间格式: {time_str}")
            
        except Exception as e:
            print(f"时间转换错误: {e}")
            return None
    
    def get_active_symbols(self, exchange_name: str, market_type: str) -> List[str]:
        """获取活跃的交易对列表"""
        try:
            exchange = self.exchanges[exchange_name]

            if market_type == 'future':
                # 使用现有的工具函数获取永续合约交易对
                if exchange_name == 'binance':
                    exchange.options['defaultType'] = 'future'
                    markets = exchange.load_markets()
                    active_symbols = get_perpetual_symbols(exchange)
                elif exchange_name == 'bybit':
                    exchange.options['defaultType'] = 'swap'
                    markets = exchange.load_markets()
                    active_symbols = get_bybit_perpetual_symbols(exchange)
                else:
                    active_symbols = []
            else:
                # 现货市场
                exchange.options['defaultType'] = 'spot'
                markets = exchange.load_markets()
                active_symbols = []

                for symbol, market in markets.items():
                    # 筛选活跃的现货交易对
                    if (market.get('active', False) and
                        market.get('spot', False) and
                        market.get('quote') in ['USDT', 'BUSD', 'USDC']):
                        active_symbols.append(symbol)

            print(f"{exchange_name} {market_type} 活跃交易对数量: {len(active_symbols)}")
            return active_symbols  # 返回所有活跃交易对，不限制数量

        except Exception as e:
            print(f"获取 {exchange_name} 交易对失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def fetch_single_symbol_data(self, symbol_info: Tuple[str, str, str, int, int]) -> Optional[Dict]:
        """获取单个交易对的K线数据和市场数据"""
        normalized_symbol, original_symbol, exchange_name, start_time, end_time = symbol_info

        try:
            exchange = self.exchanges[exchange_name]

            # 计算需要的K线数量
            duration_minutes = (end_time - start_time) // (60 * 1000)
            limit = min(duration_minutes + 10, 200)  # 多获取一些，确保覆盖时间范围

            # 获取1分钟K线数据
            klines = exchange.fetch_ohlcv(
                symbol=original_symbol,
                timeframe='1m',
                since=start_time,
                limit=limit
            )

            # 过滤出指定时间范围内的数据
            filtered_klines = []
            for kline in klines:
                if start_time <= kline[0] <= end_time:
                    filtered_klines.append(kline)

            # 获取24小时交易量数据
            volume_24h = 0
            try:
                ticker = exchange.fetch_ticker(original_symbol)
                # 优先使用quoteVolume（USDT价值），如果没有则使用baseVolume
                volume_24h = ticker.get('quoteVolume', 0) or ticker.get('baseVolume', 0) or 0
            except Exception as e:
                # 静默处理交易量获取失败
                pass

            # 获取新闻时间点的持仓量数据（通过历史数据推算）
            open_interest_at_news = 0
            try:
                if exchange_name in ['binance', 'bybit']:
                    # 获取持仓量历史数据，尝试找到接近新闻时间的数据
                    oi_history = exchange.fetch_open_interest_history(original_symbol, '1h', limit=500)
                    if oi_history:
                        news_time_ms = (start_time + end_time) // 2
                        closest_oi = None
                        min_time_diff = float('inf')

                        for oi_data in oi_history:
                            oi_timestamp = oi_data.get('timestamp', 0)
                            time_diff = abs(oi_timestamp - news_time_ms)
                            if time_diff < min_time_diff:
                                min_time_diff = time_diff
                                closest_oi = oi_data

                        if closest_oi:
                            # 优先使用美元价值，而不是合约张数
                            open_interest_at_news = closest_oi.get('openInterestValue', 0) or closest_oi.get('openInterestAmount', 0) or 0
            except Exception as e:
                # 静默处理持仓量获取失败
                pass



            return {
                'normalized_symbol': normalized_symbol,
                'original_symbol': original_symbol,
                'exchange': exchange_name,
                'klines': filtered_klines,
                'volume_24h': volume_24h,
                'open_interest': open_interest_at_news
            }

        except Exception as e:
            print(f"获取 {exchange_name} {original_symbol} 数据失败: {e}")
            return None
    
    def calculate_volatility(self, klines: List[List], news_timestamp: int, 
                           window_minutes: int) -> Dict:
        """计算价格波动指标"""
        if not klines or len(klines) < window_minutes:
            return None
            
        try:
            # 将K线数据转换为DataFrame便于处理
            df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # 找到新闻发布时刻最近的K线
            news_time = pd.to_datetime(news_timestamp, unit='ms')
            df['time_diff'] = abs(df['timestamp'] - news_time)
            news_index = df['time_diff'].idxmin()
            
            # 确保有足够的前后数据
            if news_index < window_minutes or news_index >= len(df) - window_minutes:
                return None
            
            # 新闻前X分钟的数据
            before_data = df.iloc[news_index - window_minutes:news_index]
            # 新闻后X分钟的数据  
            after_data = df.iloc[news_index:news_index + window_minutes]
            
            # 计算各种波动指标
            before_price = before_data['close'].iloc[-1]  # 新闻前最后价格
            after_max_price = after_data['high'].max()    # 新闻后最高价
            after_min_price = after_data['low'].min()     # 新闻后最低价
            after_close_price = after_data['close'].iloc[-1]  # 新闻后最后价格
            
            # 新闻前后的成交量对比
            before_volume = before_data['volume'].sum()
            after_volume = after_data['volume'].sum()
            
            # 计算波动指标
            upward_volatility = (after_max_price - before_price) / before_price * 100
            downward_volatility = (after_min_price - before_price) / before_price * 100
            net_change = (after_close_price - before_price) / before_price * 100
            max_volatility = (after_max_price - after_min_price) / after_min_price * 100
            volume_change = (after_volume - before_volume) / before_volume * 100 if before_volume > 0 else 0
            
            return {
                'before_price': float(before_price),
                'after_max_price': float(after_max_price),
                'after_min_price': float(after_min_price),
                'after_close_price': float(after_close_price),
                'upward_volatility': round(upward_volatility, 2),
                'downward_volatility': round(downward_volatility, 2),
                'net_change': round(net_change, 2),
                'max_volatility': round(max_volatility, 2),
                'volume_change': round(volume_change, 2),
                'before_volume': float(before_volume),
                'after_volume': float(after_volume)
            }
            
        except Exception as e:
            print(f"计算波动指标失败: {e}")
            return None
    
    def get_unified_symbols_with_mapping(self, market_type: str) -> Tuple[Dict[str, str], Dict[str, Dict[str, str]]]:
        """获取统一的交易对列表，去重并确定数据源优先级，同时返回原始格式映射"""
        print(f"\n📋 正在获取并整合所有交易所的 {market_type} 交易对...")

        # 一次性获取各交易所的交易对（避免重复调用）
        exchange_symbols = {}
        for exchange_name in self.exchanges.keys():
            print(f"正在获取 {exchange_name} 的交易对...")
            symbols = self.get_active_symbols(exchange_name, market_type)
            if symbols:
                exchange_symbols[exchange_name] = symbols
                print(f"{exchange_name}: {len(symbols)} 个交易对")

        if not exchange_symbols:
            print("❌ 没有获取到任何交易对")
            return {}, {}

        # 标准化交易对名称的函数
        def normalize_symbol(symbol):
            # 移除交易所特定的后缀，统一格式
            if ':' in symbol:
                return symbol.split(':')[0]  # BTC/USDT:USDT -> BTC/USDT
            return symbol

        # 标准化各交易所的交易对
        normalized_symbols = {}  # {exchange: set(normalized_symbols)}
        symbol_mapping = {}  # {normalized: {exchange: original_symbol}}

        for exchange_name, symbols in exchange_symbols.items():
            normalized_set = set()
            for symbol in symbols:
                normalized = normalize_symbol(symbol)
                normalized_set.add(normalized)

                if normalized not in symbol_mapping:
                    symbol_mapping[normalized] = {}
                symbol_mapping[normalized][exchange_name] = symbol

            normalized_symbols[exchange_name] = normalized_set

        # 计算集合关系
        binance_symbols = normalized_symbols.get('binance', set())
        bybit_symbols = normalized_symbols.get('bybit', set())

        # a1: 重合的交易对 (币安和bybit都有) → 用币安数据
        common_symbols = binance_symbols.intersection(bybit_symbols)

        # a2: 币安独有的交易对 → 用币安数据
        binance_only = binance_symbols - bybit_symbols

        # a3: bybit独有的交易对 → 用bybit数据
        bybit_only = bybit_symbols - binance_symbols

        # 构建最终的统一交易对列表
        unified_symbols = {}  # {normalized_symbol: preferred_exchange}

        # a1 + a2: 所有币安有的交易对都用币安数据
        for symbol in common_symbols.union(binance_only):
            if 'binance' in self.exchanges:
                unified_symbols[symbol] = 'binance'

        # a3: bybit独有的用bybit数据
        for symbol in bybit_only:
            if 'bybit' in self.exchanges:
                unified_symbols[symbol] = 'bybit'

        print(f"\n📊 交易对整合结果:")
        print(f"币安交易对总数: {len(binance_symbols)}")
        print(f"Bybit交易对总数: {len(bybit_symbols)}")
        print(f"重合交易对 (a1): {len(common_symbols)} → 使用币安数据")
        print(f"币安独有 (a2): {len(binance_only)} → 使用币安数据")
        print(f"Bybit独有 (a3): {len(bybit_only)} → 使用Bybit数据")
        print(f"最终统一交易对总数: {len(unified_symbols)}")

        # 验证数学关系
        expected_total = len(common_symbols) + len(binance_only) + len(bybit_only)
        print(f"验证: {len(common_symbols)} + {len(binance_only)} + {len(bybit_only)} = {expected_total}")

        return unified_symbols, symbol_mapping

    def analyze_unified_symbols(self, news_time: str, market_type: str, window_minutes: int) -> Dict:
        """分析统一的交易对列表（使用并发处理）"""
        print(f"\n🔍 开始统一分析 {market_type} 市场价格波动...")

        # 转换时间
        news_timestamp = self.convert_time_to_timestamp(news_time)
        if not news_timestamp:
            return {}

        # 计算时间范围
        start_time = news_timestamp - window_minutes * 60 * 1000
        end_time = news_timestamp + window_minutes * 60 * 1000

        # 获取统一的交易对列表和原始格式映射
        unified_symbols, symbol_mapping = self.get_unified_symbols_with_mapping(market_type)
        if not unified_symbols:
            print("❌ 没有可用的交易对")
            return {}

        # 准备并发任务数据
        symbol_tasks = []
        for normalized_symbol, exchange_name in unified_symbols.items():
            original_symbol = symbol_mapping.get(normalized_symbol, {}).get(exchange_name)
            if original_symbol:
                symbol_tasks.append((
                    normalized_symbol,
                    original_symbol,
                    exchange_name,
                    start_time,
                    end_time
                ))

        print(f"准备并发处理 {len(symbol_tasks)} 个交易对...")

        # 使用线程池并发获取K线数据
        kline_results = []
        max_workers = min(50, len(symbol_tasks))  # 限制并发数

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_symbol = {
                executor.submit(self.fetch_single_symbol_data, task): task[0]
                for task in symbol_tasks
            }

            # 收集结果
            processed = 0
            for future in as_completed(future_to_symbol):
                processed += 1
                if processed % 50 == 0:
                    print(f"已获取K线数据: {processed}/{len(symbol_tasks)} ({processed/len(symbol_tasks)*100:.1f}%)")

                try:
                    result = future.result()
                    if result and result['klines']:
                        kline_results.append(result)
                except Exception as e:
                    symbol_name = future_to_symbol[future]
                    print(f"获取 {symbol_name} 数据失败: {e}")

        print(f"✅ K线数据获取完成，有效数据: {len(kline_results)}")

        # 计算波动指标
        print("🔢 开始计算波动指标...")
        final_results = []

        for i, kline_data in enumerate(kline_results):
            try:
                # 计算波动指标
                volatility = self.calculate_volatility(
                    kline_data['klines'],
                    news_timestamp,
                    window_minutes
                )

                if volatility:
                    result = {
                        'symbol': kline_data['normalized_symbol'],
                        'original_symbol': kline_data['original_symbol'],
                        'exchange': kline_data['exchange'],
                        'volume_24h': kline_data.get('volume_24h', 0),
                        'open_interest': kline_data.get('open_interest', 0),
                        **volatility
                    }
                    final_results.append(result)

                if (i + 1) % 100 == 0:
                    print(f"已计算波动指标: {i + 1}/{len(kline_results)} ({(i + 1)/len(kline_results)*100:.1f}%)")

            except Exception as e:
                print(f"计算 {kline_data['normalized_symbol']} 波动指标失败: {e}")
                continue

        print(f"✅ 波动分析完成，最终有效数据: {len(final_results)}")
        return {
            'market_type': market_type,
            'total_symbols': len(symbol_tasks),
            'valid_results': len(final_results),
            'results': final_results
        }

    def analyze_all_exchanges(self, news_time: str, market_type: str, window_minutes: int) -> Dict:
        """分析所有交易所的价格波动（使用统一去重逻辑）"""
        print(f"\n📊 开始分析新闻事件价格影响")
        print(f"新闻时间: {news_time}")
        print(f"市场类型: {market_type}")
        print(f"分析窗口: 前后 {window_minutes} 分钟")
        print("=" * 50)

        # 使用统一的交易对分析
        unified_result = self.analyze_unified_symbols(news_time, market_type, window_minutes)

        if not unified_result or not unified_result.get('results'):
            return {
                'error': '没有获取到有效数据',
                'total_symbols': 0
            }

        # 生成综合分析报告
        return self.generate_analysis_report({}, unified_result['results'], news_time, window_minutes)

    def generate_analysis_report(self, exchange_results: Dict, all_data: List[Dict],
                               news_time: str, window_minutes: int) -> Dict:
        """生成分析报告"""
        if not all_data:
            return {
                'error': '没有获取到有效数据',
                'total_symbols': 0
            }

        # 按不同指标排序
        top_gainers = sorted(all_data, key=lambda x: x['upward_volatility'], reverse=True)[:20]
        top_losers = sorted(all_data, key=lambda x: x['downward_volatility'])[:20]
        max_volatility = sorted(all_data, key=lambda x: x['max_volatility'], reverse=True)[:20]
        volume_surge = sorted(all_data, key=lambda x: x['volume_change'], reverse=True)[:20]

        # 计算统计数据
        volatilities = [item['max_volatility'] for item in all_data]
        volume_changes = [item['volume_change'] for item in all_data if item['volume_change'] != 0]

        # 统计显著波动的币种（波动超过5%）
        significant_moves = [item for item in all_data if abs(item['max_volatility']) > 5.0]

        # 统计数据源分布
        exchange_stats = {}
        for item in all_data:
            exchange = item['exchange']
            exchange_stats[exchange] = exchange_stats.get(exchange, 0) + 1

        report = {
            'analysis_info': {
                'news_time': news_time,
                'window_minutes': window_minutes,
                'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source_distribution': exchange_stats,
                'total_symbols_analyzed': len(all_data)
            },
            'summary_statistics': {
                'total_symbols': len(all_data),
                'significant_moves_count': len(significant_moves),
                'avg_max_volatility': round(sum(volatilities) / len(volatilities), 2) if volatilities else 0,
                'max_single_volatility': max(volatilities) if volatilities else 0,
                'avg_volume_change': round(sum(volume_changes) / len(volume_changes), 2) if volume_changes else 0
            },
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'max_volatility_symbols': max_volatility,
            'volume_surge_symbols': volume_surge,
            'significant_moves': significant_moves
        }

        return report

    def print_analysis_report(self, report: Dict):
        """打印分析报告"""
        if 'error' in report:
            print(f"\n❌ 分析失败: {report['error']}")
            return

        info = report['analysis_info']
        stats = report['summary_statistics']

        print(f"\n📈 新闻事件价格影响分析报告")
        print("=" * 60)
        print(f"新闻时间: {info['news_time']}")
        print(f"分析窗口: 前后 {info['window_minutes']} 分钟")
        print(f"分析时间: {info['analysis_timestamp']}")

        # 显示数据源分布
        source_dist = info.get('data_source_distribution', {})
        if source_dist:
            source_info = ', '.join([f"{k}({v})" for k, v in source_dist.items()])
            print(f"数据源分布: {source_info}")

        print(f"总交易对数: {stats['total_symbols']}")
        print(f"显著波动数: {stats['significant_moves_count']} (波动>5%)")
        print(f"平均最大波动: {stats['avg_max_volatility']}%")
        print(f"最大单币波动: {stats['max_single_volatility']}%")
        print(f"平均成交量变化: {stats['avg_volume_change']}%")

        # 格式化数值的辅助函数
        def format_volume(volume):
            if volume >= 1e9:
                return f"{volume/1e9:.1f}B"
            elif volume >= 1e6:
                return f"{volume/1e6:.1f}M"
            elif volume >= 1e3:
                return f"{volume/1e3:.1f}K"
            else:
                return f"{volume:.0f}"

        # 打印涨幅榜前10
        print(f"\n🚀 涨幅榜 TOP 10:")
        print("-" * 120)
        print(f"{'排名':<4} {'交易对 (交易所)':<20} {'涨幅':<8} {'最大波动':<10} {'成交量变化':<12} {'24h交易量':<12} {'持仓量':<12}")
        print("-" * 120)
        for i, item in enumerate(report['top_gainers'][:10], 1):
            symbol_with_exchange = f"{item['symbol']} ({item['exchange'].upper()})"
            volume_24h_str = format_volume(item.get('volume_24h', 0))
            open_interest_str = format_volume(item.get('open_interest', 0))

            print(f"{i:<4} {symbol_with_exchange:<20} "
                  f"{item['upward_volatility']:>6.2f}% {item['max_volatility']:>8.2f}% "
                  f"{item['volume_change']:>10.2f}% {volume_24h_str:>10} "
                  f"{open_interest_str:>10}")

        # 打印跌幅榜前10
        print(f"\n📉 跌幅榜 TOP 10:")
        print("-" * 120)
        print(f"{'排名':<4} {'交易对 (交易所)':<20} {'跌幅':<8} {'最大波动':<10} {'成交量变化':<12} {'24h交易量':<12} {'持仓量':<12}")
        print("-" * 120)
        for i, item in enumerate(report['top_losers'][:10], 1):
            symbol_with_exchange = f"{item['symbol']} ({item['exchange'].upper()})"
            volume_24h_str = format_volume(item.get('volume_24h', 0))
            open_interest_str = format_volume(item.get('open_interest', 0))

            print(f"{i:<4} {symbol_with_exchange:<20} "
                  f"{item['downward_volatility']:>6.2f}% {item['max_volatility']:>8.2f}% "
                  f"{item['volume_change']:>10.2f}% {volume_24h_str:>10} "
                  f"{open_interest_str:>10}")

        # 打印成交量激增榜前10
        print(f"\n📊 成交量激增榜 TOP 10:")
        print("-" * 120)
        print(f"{'排名':<4} {'交易对 (交易所)':<20} {'成交量变化':<12} {'价格变化':<10} {'24h交易量':<12} {'持仓量':<12}")
        print("-" * 120)
        for i, item in enumerate(report['volume_surge_symbols'][:10], 1):
            if item['volume_change'] > 0:  # 只显示成交量增加的
                symbol_with_exchange = f"{item['symbol']} ({item['exchange'].upper()})"
                volume_24h_str = format_volume(item.get('volume_24h', 0))
                open_interest_str = format_volume(item.get('open_interest', 0))

                print(f"{i:<4} {symbol_with_exchange:<20} "
                      f"{item['volume_change']:>10.2f}% {item['net_change']:>8.2f}% "
                      f"{volume_24h_str:>10} {open_interest_str:>10}")

    def save_report_to_file(self, report: Dict, filename: str = None):
        """保存报告到文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"news_volatility_analysis_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n💾 分析报告已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存报告失败: {e}")


def main():
    """主函数 - 命令行接口"""
    parser = argparse.ArgumentParser(description='新闻事件价格波动分析工具')
    parser.add_argument('--time', '-t', required=True,
                       help='新闻发布时间 (格式: "YYYY-MM-DD HH:MM:SS" 或 "YYYY-MM-DD HH:MM")')
    parser.add_argument('--market', '-m', choices=['spot', 'future'], default='spot',
                       help='市场类型: spot(现货) 或 future(合约), 默认: spot')
    parser.add_argument('--window', '-w', type=int, default=5,
                       help='分析时间窗口(分钟), 默认: 5分钟')
    parser.add_argument('--save', '-s', action='store_true',
                       help='保存分析报告到JSON文件')
    parser.add_argument('--output', '-o', type=str,
                       help='指定输出文件名')

    args = parser.parse_args()

    # 创建分析器
    analyzer = NewsVolatilityAnalyzer()

    # 执行分析
    try:
        report = analyzer.analyze_all_exchanges(
            news_time=args.time,
            market_type=args.market,
            window_minutes=args.window
        )

        # 打印报告
        analyzer.print_analysis_report(report)

        # 保存报告
        if args.save:
            analyzer.save_report_to_file(report, args.output)

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断分析")
    except Exception as e:
        print(f"\n❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


"""
# 分析2024年1月15日14:30新闻对现货市场前后5分钟的影响
python NewsVolatility.py --time "2024-01-15 14:30:00" --market spot --window 5

# 分析合约市场前后10分钟的影响
python NewsVolatility.py --time "2024-01-15 14:30" --market future --window 10

# 保存分析报告到文件
python NewsVolatility.py --time "2024-01-15 14:30:00" --save

# 指定输出文件名
python NewsVolatility.py --time "2024-01-15 14:30:00" --save --output "btc_news_analysis.json"
"""