---
title: Configurations Details
description: Configure Generic (AWS Console or CLI) Acai Events
---

# Generic (AWS Console or CLI) Configurations Details

The generic event will automatically handle many common things done when eventing off a generic event invoked manually or programmatically. 
Developers then have the ability to further extend that functionality with custom middleware. 
Below is a full list of all the configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/generic) which can be deployed 
    in 1 command into your AWS account! :nerd:

## Lambda Configuration

=== "serverless.yml"

```yaml
functions:
    generic-handler:
        handler: service/handlers/generic.handle
        memorySize: 512
        timeout: 30
```

## Requirements Configuration Options

| option                      | type        | required | default                           | description                                                               |
|-----------------------------|-------------|----------|-----------------------------------|---------------------------------------------------------------------------|
| **`before`**                | func        | no       | None                              | a custom function to be ran before your records are pulled                |
| **`after`**                 | func        | no       | None                              | a custom function to be ran after your records are pulled                 |
| **`data_class`**            | class       | no       | None                              | a custom class that will be passed instead of the records object          |
| **`raise_body_error`**      | bool        | no       | False                             | will raise exception if body of record does not match schema provided     |
| **`required_body`**         | str or dict | no       | None                              | will validate body of record against this schema                          |
| **`schema`**                | str         | no       | None                              | file path pointing to the location of the openapi.yml file                |

```python
from acai_aws.firehose.requirements import requirements

# example data class
class SomeClass:
    def __init__(self, record):
        for k, v in record.body.items():
            setattr(self, k, v)

# example before function
def log_something(records, requirements):
    print(event.body) 

# example after function
def alert_something(event, result, requirements):
    if 'something' in result and 'alert' in requirements:
        print(event)

@requirements(
    before=log_something,
    data_class=SomeClass,
    raise_operation_error=True,
    raise_body_error=True,
    schema='service/openapi.yml',
    required_body='v1-generic-body', # or send jsonschema dict; schema kwarg not needed if sending jsonschema dict
    after=alert_something,
)
def handle(event):
    print(event.body)
```

## Generic Event Properties

| property                                                                     | type   | description                                          |
|------------------------------------------------------------------------------|--------|------------------------------------------------------|
| **[`body`]({{web.url}}/firehose/#recordbody)**                               | any    | can be anything, automaticallyed b64 decoded objects |


#### `event.body`

```python
print(event.body);

# output
{
    'new_data': '123456789'
}
```