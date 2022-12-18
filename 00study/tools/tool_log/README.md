# log 使用

```
tool_log
├── README.md
├── __init__.py
├── get_logger.py
├── init_logger.py
├── log.py
└── loguru_demo.py
```

## 方案 1

```bash
# get_logger
# conf/logging.conf

from tool_log.get_logger import get_logger
logger = get_logger()
logger.info(...)
```

## 方案 2

```bash
# init_logger.py
from tool_log.init_logger import Logger
logger2 = Logger(__name__).get_log()
```

## 方案 3

```bash
# __init__.py
# log.py

# usage
from tool_log import logger
logger.info("...")
```

## 其他

https://github.com/julian-west/e4ds-snippets/tree/master/best-practices/setting-up-logging
