---
title: Logger
description: How to use the Acai Logger
---

The Acai logger is automatically logs in a formatted JSON string for easy reading and searching with AWS Cloud Watch. 
A developer can then use 
[AWS filter patterns](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) making it 
effortless to find the exact log they are looking for. Below is an example of how to use the logger:


## Basic Usage

```python
from acai_aws.common import logger

logger.log(level='INFO', log='some log') # level=INFO|DEBUG|WARN|ERROR

# exammple output
"""
{
	level: '$LEVEL', 
    log: '$MESSGE'
}
"""
```
