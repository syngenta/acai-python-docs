---
title: Configurations Details
description: Configure DynamoDB Acai Events
---

# DynamoDB Configurations Details

The Dynamodb event will automatically handle many common things done when eventing off a DynamoDB stream. 
Developers then have the ability to further extend that functionality with custom middleware. 
Below is a full list of all the configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/dynamodb) which can be deployed 
    in 1 command into your AWS account! :nerd:

## Lambda Configuration

=== "Serverless Configuration"

    ```yaml
    functions:
        ddb-handler:
            handler: service/handlers/dynamodb.handle
            memorySize: 512
            timeout: 30
            events:
                - stream:
                    type: dynamodb
                    arn:
                    Fn::GetAtt: [ SomeDDBTable, StreamArn ]
    ```

=== "Handler Configuration"

    ```python
    from acai_aws.dynamodb.requirements import requirements
    from acai_aws.common import logger

    @requirements(
        before=log_something,
        operations=['created', 'deleted', 'updated'],
        data_class=SomeClass,
        raise_operation_error=True,
        raise_body_error=True,
        schema='service/openapi.yml',
        required_body='v1-ddb-body', # or jsonschema dict
        after=alert_something,
    )
    def handle(event):
        for record in event.records:
            logger.log(log=record)
        
    # example data class
    class SomeClass:
        def __init__(self, record):
            for k, v in record.body.items():
                setattr(self, k, v)

    # example before function
    def log_something(records, requirements):
        if 'something' in requirements:
            logger.log(log=records) 

    # example after function
    def alert_something(records, result, requirements):
        if 'something' in result and 'alert' in requirements:
            logger.log(log=records)
    ```

### Requirements Configuration Options

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

## DynamoDB Record Properties

| property                                                                                | type   | description                                          |
|-----------------------------------------------------------------------------------------|--------|------------------------------------------------------|
| **[`body`](/acai-python-docs/dynamodb/configuration-details/#recordbody)**              | object | the new image of dynamodb record; created or updated |
| **[`created`](/acai-python-docs/dynamodb/configuration-details/#recordcreated)**        | float  | the approximate creationDate time                    |
| **[`expired`](/acai-python-docs/dynamodb/configuration-details/#recordexpired)**        | bool   | whether the ttl has expired                          |
| **[`id`](/acai-python-docs/dynamodb/configuration-details/#recordid)**                  | str    | the id of the event which invoked the lambda         |
| **[`identity`](/acai-python-docs/dynamodb/configuration-details/#recordidentity)**      | object | the identity who triggered the dynamodb change       |
| **[`keys`](/acai-python-docs/dynamodb/configuration-details/#recordkeys)**              | object | the keys of DynamoDB record                          |
| **[`name`](/acai-python-docs/dynamodb/configuration-details/#recordname)**              | str    | the name of the event which invoked the lambda       |
| **[`new_image`](/acai-python-docs/dynamodb/configuration-details/#recordnewimage)**     | object | the new image of dynamodb record; created or updated |
| **[`old_image`](/acai-python-docs/dynamodb/configuration-details/#recordoldimage)**     | object | the old image of dynamodb record; updated or deleted |
| **[`operation`](/acai-python-docs/dynamodb/configuration-details/#recordoperation)**    | str    | triggered operation lambda (create, update, delete)  |
| **[`region`](/acai-python-docs/dynamodb/configuration-details/#recordregion)**          | str    | the region the record is from                        |
| **[`size`](/acai-python-docs/dynamodb/configuration-details/#recordsize)**              | int    | the size in bytes of the record                      |
| **[`source`](/acai-python-docs/dynamodb/configuration-details/#recordsource)**          | str    | the source of the event which invoked the lambda     |
| **[`source_arn`](/acai-python-docs/dynamodb/configuration-details/#recordsourcearn)**   | str    | the event source arn                                 |
| **[`stream_type`](/acai-python-docs/dynamodb/configuration-details/#recordstreamtype)** | str    | the stream view type                                 |
| **[`version`](/acai-python-docs/dynamodb/configuration-details/#recordversion)**        | str    | the event version                                    |
| **[`operation`](/acai-python-docs/dynamodb/configuration-details/#recordoperation)**    | str    | enum of `created`, `deleted`, `updated`              |

#### `record.region`

```python
print(record.region);

# output
'us-east-2'
```

#### `record.id`

```python
print(record.id);

# output
'9a37c0d03eb60f7cf70cabc823de9907'
```

#### `record.name`

```python
print(record.name);

# output
'INSERT'
```

#### `record.source`

```python
print(record.source);

# output
'aws:dynamodb'
```

#### `record.keys`

???+ info
    This is converted from the original DDB JSON to standard json

```python
print(record.keys);

# output
{
    'example_id': '123456789'
}
```

#### `record.old_image`

???+ info
    This is converted from the original DDB JSON to standard json

```python
print(record.old_image);

# output
{
    'old_data': '123456789'
}
```

#### `record.new_image`

???+ info
    This is converted from the original DDB JSON to standard json

```python
print(record.new_image);

# output
{
    'new_data': '123456789'
}
```

#### `record.body`

???+ info
    This is converted from the original DDB JSON to standard json from `new_image`

```python
print(record.body);

# output
{
    'new_data': '123456789'
}
```

#### `record.operation`

```python
print(record.operation);

# output
'create'
```

#### `record.source_arn`

```python
print(record.source_arn);

# output
'arn:aws:dynamodb:us-east-1:771875143460:table/test-example/stream/2019-10-04T23:18:26.340'
```

#### `record.version`

```python
print(record.version);

# output
'1.1'
```

#### `record.stream_type`

```python
print(record.stream_type);

# output
'NEW_AND_OLD_IMAGES'
```

#### `record.size`

```python
print(record.size);

# output
1124
```

#### `record.created`

```python
print(record.created);

# output (unix timestamp)
1538695200.0 
```

#### `record.identity`

```python
print(record.identity);

# output
{
    'type': 'Service',
    'principalId': 'dynamodb.amazonaws.com'
}
```

#### `record.expired`

```python
print(record.expired);

# output
False
```
