---
title: Configurations Details
description: Configure Firehose Acai Events
---

# Firehose Configurations Details

The firehose event will automatically handle many common things done when eventing off a firehose stream. 
Developers then have the ability to further extend that functionality with custom middleware. 
Below is a full list of all the configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/firehose) which can be deployed 
    in 1 command into your AWS account! :nerd:

## Lambda Configuration

=== "serverless.yml"

```yaml
functions:
    firehose-handler:
        handler: service/handlers/firehose.handle
        memorySize: 512
        timeout: 30
        events:
            - stream:
                type: firehose
                arn:
                  Fn::GetAtt: [ MyfirehoseStream, Arn ]
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
from acai.firehose.requirements import requirements

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
    data_class=SomeClass,
    raise_operation_error=True,
    raise_body_error=True,
    schema='service/openapi.yml',
    required_body='v1-firehose-body', # or send jsonschema dict; schema kwarg not needed if sending jsonschema dict
    after=alert_something,
)
def handle(event):
    for record in event.records:
        print(record)
```

## Firehose Record Properties

| property                                                                     | type   | description                                          |
|------------------------------------------------------------------------------|--------|------------------------------------------------------|
| **[`record_id`]({{web.url}}/firehose/#recordrecord_id)**                     | str    | record id of the stream                              |
| **[`epoc_time_stamp`]({{web.url}}/firehose/#recordepoc_time_stamp)**         | int    | epoc time stamp of the stream                        |
| **[`shard_id`]({{web.url}}/firehose/#recordshard_id)**                       | str    | shard id arn of the stream                           |
| **[`subsequence_number`]({{web.url}}/firehose/#recordvsubsequence_number)**  | str    | subsequence number arn of the stream                 |
| **[`partition_key`]({{web.url}}/firehose/#recordpartition_key)**             | str    | partition key                                        |
| **[`time_stamp`]({{web.url}}/firehose/#recordtime_stamp)**                   | str    | time stamp                                           |
| **[`sequence_number`]({{web.url}}/firehose/#recordsequence_number)**         | str    | sequence number                                      |
| **[`data`]({{web.url}}/firehose/#recorddata)**                               | any    | can be anything, automaticallyed b64 decoded objects |
| **[`body`]({{web.url}}/firehose/#recordbody)**                               | any    | can be anything, automaticallyed b64 decoded objects |


#### `record.record_id`

```python
print(record.record_id);

# output
'record1'
```

#### `record.epoc_time_stamp`

```python
print(record.epoc_time_stamp);

# output
1510772160000
```

#### `record.shard_id`

```python
print(record.shard_id);

# output
'shardId-000000000000'
```

#### `record.subsequence_number`

```python
print(record.subsequence_number);

# output
''
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