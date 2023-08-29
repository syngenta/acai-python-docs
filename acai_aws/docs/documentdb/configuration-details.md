---
title: Configurations Details
description: Configure DocumentDB Acai Events
---

# DocumentDB Configurations Details

The DocumentDB event will automatically handle many common things done when eventing off a DocumentDB stream. 
Developers then have the ability to further extend that functionality with custom middleware. 
Below is a full list of all the configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/documentdb) which can be deployed 
    in 1 command into your AWS account! :nerd:

## Lambda Configuration

=== "serverless.yml"

```yaml
functions:
    documentdb-handler:
        handler: service/handlers/documentdb.handle
        memorySize: 512
        timeout: 30
        events:
            - stream:
                type: documentdb
                arn:
                    Fn::GetAtt: [ SomeDocDBCluser, ClusterArn ]
```

## Requirements Configuration Options

| option                      | type        | required | default                           | description                                                               |
|-----------------------------|-------------|----------|-----------------------------------|---------------------------------------------------------------------------|
| **`before`**                | func        | no       | None                              | a custom function to be ran before your records are pulled                |
| **`after`**                 | func        | no       | None                              | a custom function to be ran after your records are pulled                 |
| **`data_class`**            | class       | no       | None                              | a custom class that will be passed instead of the records object          |
| **`operations`**            | list        | no       | ['created', 'updated', 'deleted'] | will only run if record was created from the listed operation             |
| **`raise_operation_error`** | bool        | no       | False                             | will raise exception if operation of record is not from listed operations |
| **`raise_body_error`**      | bool        | no       | False                             | will raise exception if body of record does not match schema provided     |
| **`required_body`**         | str or dict | no       | None                              | will validate body of record against this schema                          |
| **`schema`**                | str         | no       | None                              | file path pointing to the location of the openapi.yml file                |

```python
from acai_aws.documentdb.requirements import requirements

# example data class
class SomeClass:
    def __init__(self, record):
        for k, v in record.body.items():
            setattr(self, k, v)

# example before function
def log_something(records, requirements):
    if 'something' in requirements:
        print(records) 

# example after function
def alert_something(records, result, requirements):
    if 'something' in result and 'alert' in requirements:
        print(records)

@requirements(
    before=log_something,
    operations=['created', 'deleted', 'updated'],
    data_class=SomeClass,
    raise_operation_error=True,
    raise_body_error=True,
    schema='service/openapi.yml',
    required_body='v1-docdb-body', # or send jsonschema dict; schema kwarg not needed if sending jsonschema dict
    after=alert_something,
)
def handle(event):
    for record in event.records:
        print(record)
```

## DocumentDB Record Properties

| property                                                    | type   | description                                          |
|-------------------------------------------------------------|--------|------------------------------------------------------|
| **[`body`]({{web.url}}/dynamodb/#recordbody)**              | object | the new image of dynamodb record; created or updated |


#### `record.region`

```python
print(record.region);

# output
'us-east-2'
```

