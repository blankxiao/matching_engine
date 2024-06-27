# Matching Engine

这是一个简单的匹配引擎项目，用于处理买卖订单并生成交易记录。

## 项目结构

```
matchingEngine/
├── matching_engine/
│   ├── __init__.py
│   ├── Order.py
│   ├── OrderBook.py
│   ├── Trade.py
│   ├── TradingDao.py
├── .gitignore
└── cli.py
```

### 文件说明

- `matching_engine/`
  - `__init__.py`: 初始化模块。
  - `Order.py`: 包含订单类。
  - `OrderBook.py`: 包含订单簿类，用于管理订单的添加和匹配。
  - `Trade.py`: 包含交易类。
  - `TradingDao.py`: 数据访问对象类，用于与数据库交互。
- `.gitignore`: Git 忽略文件列表。
- `cli.py`: 命令行接口，用于手动测试匹配引擎。



### 运行命令行接口
通过查看帮助
```bash
python cli.py --help
```
