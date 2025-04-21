# 价格监控系统

这是一个用于监控加密货币市场价格波动的系统，支持多种策略和多交易所数据。

## 项目结构

- `main.py` - 主程序入口，负责启动不同的策略
- `utils.py` - 通用工具函数和基类
- `price_volatility_strategy.py` - 价格异动监控策略
- `market_data_strategy.py` - 永续合约市场数据策略
- `requirements.txt` - 项目依赖列表
- `perpetual_symbols.json` - 存储永续合约交易对列表
- `coin.txt` - 重点关注的币种列表
- `DEMO.py` - 示例代码

## 功能特点

- 支持多策略同时运行
- 自动检测新交易对
- 价格波动监控
- 市场数据分析
- 邮件通知功能

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保已安装所有依赖
2. 运行主程序:

```bash
python main.py
```

3. 在菜单中选择要运行的策略:
   - 1: 价格异动策略
   - 2: 永续合约市场数据策略
   - 0: 同时运行所有策略

## 配置说明

- 代理设置: 如需修改代理配置，请编辑 `utils.py` 中的 `get_socks5_proxy()` 函数
- 邮件配置: 邮件通知相关配置在 `utils.py` 中设置

## 项目架构

项目采用模块化设计，主要组件包括:

1. 策略基类 (Strategy): 所有策略的抽象基类
2. 具体策略实现:
   - PriceVolatilityStrategy: 监控价格异动
   - MarketDataStrategy: 分析市场数据
3. 通用工具模块: 提供共享功能

### 架构改进

本项目已进行全面重构，主要改进包括：

1. **策略抽象**: 创建了 `Strategy` 抽象基类，统一了策略的接口
2. **功能共享**: 将共用功能抽象到 `utils.py` 中，避免代码重复
3. **模块化设计**: 每个文件负责特定功能，降低了代码耦合度
4. **统一异常处理**: 规范化了异常处理流程
5. **标准化接口**: 使不同策略具有相同的生命周期管理

## 自定义策略

要创建新的策略，只需:

1. 继承 `Strategy` 基类
2. 实现 `initialize()` 和 `execute()` 方法
3. 在 `main.py` 中添加对新策略的支持

```python
from utils import Strategy

class MyCustomStrategy(Strategy):
    def __init__(self):
        super().__init__("我的自定义策略")
        # 初始化自定义属性

    def initialize(self):
        # 初始化逻辑
        self.is_running = True

    def execute(self):
        # 策略执行逻辑
        while self.is_running:
            # 实现您的策略逻辑
            pass
```

## 注意事项

- 程序需要网络连接
- 对于国内用户，可能需要配置代理
- API访问频率有限制，请注意调整请求频率
- 使用API密钥时注意安全，避免泄露

## 故障排除指南

### Pandas 警告

如果您看到类似以下的 Pandas SettingWithCopyWarning 警告：
```
SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
```

这些警告已在最新版本中修复，如果您仍然看到它们，请更新代码或忽略它们，它们不会影响程序功能。

### 无法获取市值数据

如果看到类似以下的消息：
```
警告: XXX 没有市值数据，无法计算成交量/市值比
```

这是因为该币种在预设的市值数据库中不存在。解决方法:

1. 如果需要为更多币种添加市值数据，您可以编辑 `utils.py` 文件中的 `get_cryptocurrency_marketcap` 函数，在 `market_caps` 字典中添加更多币种的市值。

2. 启用外部API获取：在 `MarketDataStrategy` 类的 `__init__` 方法中设置:
   ```python
   self.use_external_api = True
   ```
   然后实现 `get_cryptocurrency_marketcap` 函数中的外部API调用部分。

### 无法获取4小时持仓量变化

首次运行程序时，由于没有历史数据，无法计算持仓量变化。第二次运行时（至少等待4小时后）将自动解决此问题。

### 与交易所API连接问题

如果收到连接错误或API限制错误：

1. 检查您的网络连接
2. 确保代理设置正确（如果使用）
3. 在 `utils.py` 中增加 `timeout` 和 `retries` 参数

### 数据显示 "nan%" 或 "--"

- "nan%" 表示计算结果是 NaN (Not a Number)，可能是由于除以零或数据缺失
- "--" 是一个友好的占位符，表示数据不可用

### 如何添加更多交易所支持

在 `MarketDataStrategy` 类的 `initialize` 方法中已支持 Bybit、OKX 和 Binance，如需添加更多交易所，请按照同样的格式添加到 `self.exchanges` 字典中。 