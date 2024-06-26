---
title: Configurations Details
description: Configure Kinesis Acai Events
---

# Kinesis Configurations Details

The kinesis event will automatically handle many common things done when eventing off a kinesis stream. 
Developers then have the ability to further extend that functionality with custom middleware. 
Below is a full list of all the configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/kinesis) which can be deployed 
    in 1 command into your AWS account! :nerd:

## Lambda Configuration

=== "Serverless Configuration"

    ```yaml
    functions:
        kinesis-handler:
            handler: service/handlers/kinesis.handle
            memorySize: 512
            timeout: 30
            events:
                - stream:
                    type: kinesis
                    arn:
                    Fn::GetAtt: [ MyKinesisStream, Arn ]
    ```

=== "Handler Configuration"

    ```python
    from acai_aws.kinesis.requirements import requirements
    from acai_aws.common import logger

    @requirements(
        before=log_something,
        data_class=SomeClass,
        raise_operation_error=True,
        raise_body_error=True,
        schema='service/openapi.yml',
        required_body='v1-kinesis-body', # or jsonschema dict
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
| **`raise_body_error`**      | bool        | no       | False                             | will raise exception if body of record does not match schema provided     |
| **`required_body`**         | str or dict | no       | None                              | will validate body of record against this schema                          |
| **`schema`**                | str         | no       | None                              | file path pointing to the location of the openapi.yml file                |

## Kinesis Record Properties

| property                                                                    | type   | description                                          |
|-----------------------------------------------------------------------------|--------|------------------------------------------------------|
| **[`id`](/acai-python-docs/kinesis/configuration-details/#recordid)**                                   | str    | id of the stream                                     |
| **[`name`](/acai-python-docs/kinesis/configuration-details/#recordname)**                               | str    | name of the stream                                   |
| **[`source_arn`](/acai-python-docs/kinesis/configuration-details/#recordsource_arn)**                   | str    | source arn of the stream                             |
| **[`region`](/acai-python-docs/kinesis/configuration-details/#recordregion)**                           | str    | region arn of the stream                             |
| **[`version`](/acai-python-docs/kinesis/configuration-details/#recordversion)**                         | str    | version arn of the stream                            |
| **[`invoke_identity_arn`](/acai-python-docs/kinesis/configuration-details/#recordinvoke_identity_arn)** | str    | arn of the indentity                                 |
| **[`schema_version`](/acai-python-docs/kinesis/configuration-details/#recordschema_version)**           | str    | schema version                                       |
| **[`partition_key`](/acai-python-docs/kinesis/configuration-details/#recordpartition_key)**             | str    | partition key                                        |
| **[`time_stamp`](/acai-python-docs/kinesis/configuration-details/#recordtime_stamp)**                   | str    | time stamp                                           |
| **[`sequence_number`](/acai-python-docs/kinesis/configuration-details/#recordsequence_number)**         | str    | sequence number                                      |
| **[`data`](/acai-python-docs/kinesis/configuration-details/#recorddata)**                               | any    | can be anything, automaticallyed b64 decoded objects |
| **[`body`](/acai-python-docs/kinesis/configuration-details/#recordbody)**                               | any    | can be anything, automaticallyed b64 decoded objects |


#### `record.id`

```python
print(record.id);

# output
'shardId-000000000006:49590338271490256608559692538361571095921575989136588898'
```

#### `record.name`

```python
print(record.name);

# output
'aws:kinesis:record'
```

#### `record.source_arn`

```python
print(record.source_arn);

# output
'arn:aws:kinesis:us-east-2:123456789012:stream/lambda-stream'
```

#### `record.region`

```python
print(record.region);

# output
'us-east-2'
```

#### `record.version`

```python
print(record.version);

# output
'1.0'
```

#### `record.invoke_identity_arn`

```python
print(record.invoke_identity_arn);

# output
'arn:aws:iam::123456789012:role/lambda-role'
```

#### `record.schema_version`

```python
print(record.schema_version);

# output
'1.0'
```

#### `record.partition_key`

```python
print(record.partition_key);

# output
'1'
```

#### `record.time_stamp`

```python
print(record.time_stamp);

# output
1545084650.987
```

#### `record.sequence_number`

```python
print(record.sequence_number);

# output
49590338271490256608559692538361571095921575989136588898
```

#### `record.data`

```python
print(record.data);

# output
{
    'new_data': '123456789'
}
```

#### `record.body`

```python
print(record.body);

# output
{
    'new_data': '123456789'
}
```