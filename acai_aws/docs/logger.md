---
title: Logger
description: How to use the Acai Logger
---

The Acai logger is automatically logs in a formatted JSON string for easy reading and searching with AWS Cloud Watch. 
It also supports basic inline logging for better local development debugging.
A developer can then use 
[AWS filter patterns](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) making it 
effortless to find the exact log they are looking for. You can use an environmnet variable to change the format of the
log to make working locally.

Below is an example of how to use the logger:

## Basic Usage

```python
import os

from acai_aws.common import logger

os.getenv['LOG_FORMAT'] = 'JSON' # INLINE (great for local development)
os.getenv['LOG_LEVEL'] = 'INFO' # WARN|ERROR

logger.log(level='INFO', log='some log') # level=INFO|DEBUG|WARN|ERROR

# exammple output
"""
{
	level: '$LEVEL', 
    "time": "2023-09-01T19:35:06.163634+00:00",
    "error_trace": [
        "Traceback (most recent call last):",
        "File \"/some-directory/router.py\", line 36, in route",
        "self.__run_route_procedure(request, response)",
        "File \"/some-directory/router.py\", line 53, in __run_route_procedure",
        "endpoint.run(request, response)",
        "File \"/some-directory/endpoint.py\", line 32, in run",
        "return self.__method(request, response)",
        "File \"/some-directory/requirements.py\", line 21, in run_method",
        "func(request, response)",
        "File \"api/v1/handler/grower/_grower_id.py\", line 8, in get",
        "grower = Grower.get_by_id(grower_id=request.path_params['grower_id_HERE'])",
        "KeyError: 'grower_id_HERE'"
    ],
    log: '$MESSGE'
}
"""
```

## Decorator Usage

The Acai logger also comes packaged as an easy to use log decorator that can decorate any method or function and even apply log conditions so you can
control when exactly something is logged.


```python
from acai_aws.common.logger.decorator import log

@log()
def example_simple(arg1, arg2, **kwargs):
    return {'args': [arg1, arg2], 'kwargs': kwargs}

@log(level='INFO')
def example_level(arg1, arg2, **kwargs):
    return {'args': [arg1, arg2], 'kwargs': kwargs}

@log(level='INFO', condition=some_log_condition)
def example_condition(arg1, arg2, **kwargs):
    return {'args': [arg1, arg2], 'kwargs': kwargs}

def some_log_condition(*args, **_):
    if args[0] == 1:
        return True
    return False

```