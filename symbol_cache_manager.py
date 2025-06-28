"""
交易对缓存管理器
用于优化NewsVolatility的交易对获取性能
"""

import json
import os
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class SymbolCacheManager:
    """交易对缓存管理器"""
    
    def __init__(self, cache_dir: str = None):
        """
        初始化缓存管理器

        Args:
            cache_dir: 缓存目录，默认为market_data目录
        """
        if cache_dir:
            self.cache_dir = cache_dir
        else:
            # 默认使用market_data目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.cache_dir = os.path.join(current_dir, "market_data")

        # 确保缓存目录存在
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, "symbols_cache.json")
        self.cache_ttl = 3600  # 缓存1小时过期
        self.memory_cache = {}  # 内存缓存
        self.memory_cache_ttl = 300  # 内存缓存5分钟过期
        
    def _get_cache_key(self, market_type: str, exchange: str = "all") -> str:
        """生成缓存键"""
        return f"{exchange}_{market_type}"
    
    def _is_cache_expired(self, timestamp: float, ttl: int) -> bool:
        """检查缓存是否过期"""
        return time.time() - timestamp > ttl
    
    def load_file_cache(self) -> Dict:
        """从文件加载缓存"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                print(f"✅ 从文件加载缓存: {self.cache_file}")
                return cache_data
        except Exception as e:
            print(f"⚠️ 加载缓存文件失败: {e}")
        
        return {}
    
    def save_file_cache(self, cache_data: Dict) -> bool:
        """保存缓存到文件"""
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 缓存已保存到: {self.cache_file}")
            return True
        except Exception as e:
            print(f"❌ 保存缓存失败: {e}")
            return False
    
    def get_cached_symbols(self, market_type: str, exchange: str = "all") -> Optional[Tuple[Dict, Dict]]:
        """
        获取缓存的交易对数据
        
        Args:
            market_type: 市场类型 (spot/future)
            exchange: 交易所名称，默认"all"表示所有交易所
            
        Returns:
            (unified_symbols, symbol_mapping) 或 None
        """
        cache_key = self._get_cache_key(market_type, exchange)
        
        # 1. 先检查内存缓存
        if cache_key in self.memory_cache:
            cache_entry = self.memory_cache[cache_key]
            if not self._is_cache_expired(cache_entry['timestamp'], self.memory_cache_ttl):
                print(f"🚀 使用内存缓存: {cache_key}")
                return cache_entry['unified_symbols'], cache_entry['symbol_mapping']
        
        # 2. 检查文件缓存
        file_cache = self.load_file_cache()
        if cache_key in file_cache:
            cache_entry = file_cache[cache_key]
            if not self._is_cache_expired(cache_entry['timestamp'], self.cache_ttl):
                print(f"📁 使用文件缓存: {cache_key}")
                
                # 更新内存缓存
                self.memory_cache[cache_key] = cache_entry
                
                return cache_entry['unified_symbols'], cache_entry['symbol_mapping']
            else:
                print(f"⏰ 文件缓存已过期: {cache_key}")
        
        print(f"❌ 没有有效缓存: {cache_key}")
        return None
    
    def update_cache(self, market_type: str, unified_symbols: Dict, symbol_mapping: Dict, exchange: str = "all") -> bool:
        """
        更新缓存数据
        
        Args:
            market_type: 市场类型
            unified_symbols: 统一交易对字典
            symbol_mapping: 交易对映射字典
            exchange: 交易所名称
            
        Returns:
            是否更新成功
        """
        cache_key = self._get_cache_key(market_type, exchange)
        timestamp = time.time()
        
        cache_entry = {
            'unified_symbols': unified_symbols,
            'symbol_mapping': symbol_mapping,
            'timestamp': timestamp,
            'created_at': datetime.now().isoformat(),
            'market_type': market_type,
            'exchange': exchange,
            'symbol_count': len(unified_symbols)
        }
        
        # 更新内存缓存
        self.memory_cache[cache_key] = cache_entry
        
        # 更新文件缓存
        file_cache = self.load_file_cache()
        file_cache[cache_key] = cache_entry
        
        success = self.save_file_cache(file_cache)
        if success:
            print(f"✅ 缓存已更新: {cache_key} ({len(unified_symbols)} 个交易对)")
        
        return success
    
    def get_cache_info(self) -> Dict:
        """获取缓存信息"""
        info = {
            'cache_file': self.cache_file,
            'cache_ttl': self.cache_ttl,
            'memory_cache_ttl': self.memory_cache_ttl,
            'memory_cache_keys': list(self.memory_cache.keys()),
            'file_cache_exists': os.path.exists(self.cache_file)
        }
        
        if info['file_cache_exists']:
            file_cache = self.load_file_cache()
            info['file_cache_keys'] = list(file_cache.keys())
            info['file_cache_entries'] = []
            
            for key, entry in file_cache.items():
                age_seconds = time.time() - entry['timestamp']
                is_expired = self._is_cache_expired(entry['timestamp'], self.cache_ttl)
                
                info['file_cache_entries'].append({
                    'key': key,
                    'symbol_count': entry.get('symbol_count', 0),
                    'created_at': entry.get('created_at', 'unknown'),
                    'age_seconds': int(age_seconds),
                    'age_minutes': int(age_seconds / 60),
                    'is_expired': is_expired
                })
        
        return info
    
    def clear_cache(self, cache_type: str = "all") -> bool:
        """
        清空缓存
        
        Args:
            cache_type: 缓存类型 ("memory", "file", "all")
        """
        try:
            if cache_type in ["memory", "all"]:
                self.memory_cache.clear()
                print("✅ 内存缓存已清空")
            
            if cache_type in ["file", "all"]:
                if os.path.exists(self.cache_file):
                    os.remove(self.cache_file)
                    print("✅ 文件缓存已清空")
            
            return True
        except Exception as e:
            print(f"❌ 清空缓存失败: {e}")
            return False
    
    def force_refresh_symbols(self, market_type: str, get_symbols_func) -> Optional[Tuple[Dict, Dict]]:
        """
        强制刷新交易对数据
        
        Args:
            market_type: 市场类型
            get_symbols_func: 获取交易对的函数
            
        Returns:
            (unified_symbols, symbol_mapping) 或 None
        """
        try:
            print(f"🔄 强制刷新 {market_type} 交易对数据...")
            unified_symbols, symbol_mapping = get_symbols_func(market_type)
            
            if unified_symbols:
                self.update_cache(market_type, unified_symbols, symbol_mapping)
                return unified_symbols, symbol_mapping
            else:
                print("❌ 获取交易对数据失败")
                return None
                
        except Exception as e:
            print(f"❌ 强制刷新失败: {e}")
            return None
