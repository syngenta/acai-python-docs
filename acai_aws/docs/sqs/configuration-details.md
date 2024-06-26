---
title: Configurations
description: Configure SQS Acai Events
---

# SQS Event Configurations

The SQS event will automatically handle many common things done when eventing off an SQS stream. Developers 
then have the ability to further extend that functionality with custom middleware. Below is a full list of all the 
configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/sqs) which can be deployed in 1 
    command into your AWS account! :nerd:

## Lambda Configuration

=== "Serverless Configuration"

    ```yaml
    functions:
        sqs-handler:
            handler: service/handlers/sqs.handle
            memorySize: 512
            timeout: 900
            events:
                - sqs:
                    arn:
                        Fn::GetAtt: [ SomeQueue, 'Arn' ]
    ```

=== "Handler Configuration"

    ```python
    from acai.sqs.requirements import requirements
    from acai_aws.common import logger

    @requirements(
        before=log_something,
        data_class=SomeClass,
        raise_body_error=True,
        schema='service/openapi.yml',
        required_body='v1-sqs-body', # or jsonschema dict
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

| option                 | type        | required | default | description                                                           |
|------------------------|-------------|----------|---------|-----------------------------------------------------------------------|
| **`before`**           | func        | no       | None    | a custom function to be ran before your records are pulled            |
| **`after`**            | func        | no       | None    | a custom function to be ran after your records are pulled             |
| **`data_class`**       | class       | no       | None    | a custom class that will be passed instead of the records object      |
| **`raise_body_error`** | bool        | no       | False   | will raise exception if body of record does not match schema provided |
| **`required_body`**    | str or dict | no       | None    | will validate body of record against this schema                      |
| **`schema`**           | str         | no       | None    | file path pointing to the location of the openapi.yml file            |

## SQS Record Properties

| property                                                                                          | type     | description                                                                       |
|---------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------|
| **[`source`](/acai-python-docs/sqs/configuration-details/#recordsource)**                         | str      | the source of the event                                                           |
| **[`source_arn`](/acai-python-docs/sqs/configuration-details/#recordsource_arn)**                 | str      | the source arn of the event                                                       |
| **[`region`](/acai-python-docs/sqs/configuration-details/#recordregion)**                         | str      | the region of the event                                                           |
| **[`body`](/acai-python-docs/sqs/configuration-details/#recordbody)**                             | dict,str | the body sqs message                                                              |
| **[`md5_of_body`](/acai-python-docs/sqs/configuration-details/#recordmd5_of_body)**               | str      | the md5 of the body                                                               |
| **[`attributes`](/acai-python-docs/sqs/configuration-details/#recordattributes)**                 | dict     | the attributes dict of the message attributes; easier than use message attributes |
| **[`message_attributes`](/acai-python-docs/sqs/configuration-details/#recordmessage_attributes)** | dict     | the message attributes of the message                                             |

#### `record.source`

```python
print(record.source)

# output
'aws:sqs'
```

#### `record.source_arn`

```python
print(record.source_arn)

# output
'arn:aws:sqs:us-east-2:123456789012:my-queue'
```

#### `record.region`

```python
print(record.region)

# output
'us-east-1'
```

#### `record.body`

```python
print(record.body)

# output
{
    'key': 'value'
}
```

#### `record.md5_of_body`

```python
print(record.md5_of_body)

# output
'e4e68fb7bd0e697a0ae8f1bb342846b3'
```

#### `record.attributes`

```python
print(record.attributes)

# output
{
    'SomeString': 'Some String',
    'SomeBinary': 'Some Binary',
}
```

#### `record.message_attributes`

```python
print(record.message_attributes)

# output
{
    'SomeString': {
        'DataType': 'string',
        'StringValue': 'Some String'
    },
    'SomeBinary': {
        'DataType': 'binary',
        'BinaryValue': 'Some Binary'
    }
}
```
