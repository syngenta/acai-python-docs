---
title: Configurations Details
description: Configure S3 Acai Events
---

# S3 Configurations Details

The S3 event will automatically handle many common things done when eventing off a S3 event. Developers then have the 
ability to further extend that functionality with custom middleware. Below is a full list of all the configurations 
available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/s3) which can be deployed in 1 
    command into your AWS account! :nerd:

## Lambda Configuration

=== "serverless.yml"

```yaml
functions:
    s3-handler:
        handler: service/handlers/s3.handle
        memorySize: 512
        timeout: 900
        events:
            - s3:
                bucket: uploadsBucket
                event: s3:ObjectCreated:*
```

## Requirements Configuration Options

| option                      | type        | required | default                           | description                                                               |
|-----------------------------|-------------|----------|-----------------------------------|---------------------------------------------------------------------------|
| **`before`**                | func        | no       | None                              | a custom function to be ran before your records are pulled                |
| **`after`**                 | func        | no       | None                              | a custom function to be ran after your records are pulled                 |
| **`data_class`**            | class       | no       | None                              | a custom class that will be passed instead of the records object          |
| **`data_type`**             | enum (str)  | no       | ['json', 'csv']                   | will convert data to a dict based on type; `requires get_object=True`     |
| **`get_object`**            | bool        | no       | False                             | will download object from s3 bucket and hold in memory                    |
| **`operations`**            | list        | no       | ['created', 'updated', 'deleted'] | will only run if record was created from the listed operation             |
| **`raise_operation_error`** | bool        | no       | False                             | will raise exception if operation of record is not from listed operations |
| **`raise_body_error`**      | bool        | no       | False                             | will raise exception if body of record does not match schema provided     |
| **`required_body`**         | str or dict | no       | None                              | will validate body of record against this schema                          |
| **`schema`**                | str         | no       | None                              | file path pointing to the location of the openapi.yml file                |

```python
from acai.s3.requirements import requirements

# example data class (requires, get_object=True and a data_type)
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
    get_object=True,
    data_type='json',
    data_class=SomeClass,
    raise_body_error=True, # requires, get_object=True and a data_type
    schema='service/openapi.yml',
    required_body='v1-s3-body', # or send jsonschema dict; schema kwarg not needed if sending jsonschema dict
    after=alert_something,
)
def handle(event):
    for record in event.records:
        print(record)
```

## S3 Record Properties

| property                                                         | type       | description                             |
|------------------------------------------------------------------|------------|-----------------------------------------|
| **[`name`]({{web.url}}/s3/#recordname)**                         | str        | the name of the event                   |
| **[`source`]({{web.url}}/s3/#recordsource)**                     | str        | the source of the event                 |
| **[`version`]({{web.url}}/s3/#recordversion)**                   | str        | the version of the event                |
| **[`time`]({{web.url}}/s3/#recordtime)**                         | str        | the time of the event                   |
| **[`region`]({{web.url}}/s3/#recordregion)**                     | str        | the region of the event                 |
| **[`request`]({{web.url}}/s3/#recordrequest)**                   | dict       | the request parameters of the event     |
| **[`response`]({{web.url}}/s3/#recordresponse)**                 | dict       | the response parameters of the event    |
| **[`configuration_id`]({{web.url}}/s3/#recordconfiguration_id)** | str        | the configuration id                    |
| **[`object`]({{web.url}}/s3/#recordobject)**                     | dict       | the object dict of the event            |
| **[`bucket`]({{web.url}}/s3/#recordbucket)**                     | dict       | the bucket dict of the event            |
| **[`bucket`]({{web.url}}/s3/#recordbucket)**                     | dict       | the bucket dict of the event            |
| **[`bucket_arn`]({{web.url}}/s3/#recordbucket_arn)**             | str        | the arn of the bucket                   |
| **[`bucket_owner`]({{web.url}}/s3/#recordbucket_owner)**         | str        | the owner of the bucket                 |
| **[`key`]({{web.url}}/s3/#recordkey)**                           | str        | the key owner of the object             |
| **[`schema_version`]({{web.url}}/s3/#recordschema_version)**     | str        | the schema version                      |
| **[`user_identity`]({{web.url}}/s3/#recorduser_identity)**       | str        | the user identity                       |
| **[`operation`]({{web.url}}/s3/#recordoperation)**               | enum (str) | enum of `created`, `deleted`, `updated` |
| **[`body`]({{web.url}}/s3/#recordbody)**                         | dict,bytes | the body of file in the s3 bucket       |

#### `record.name`

```python
print(record.name)

# output
'ObjectRemoved: Put'
```

#### `record.source`

```python
print(record.source)

# output
'aws:s3'
```

#### `record.version`

```python
print(record.version)

# output
'2.0'
```

#### `record.time`

```python
print(record.time)

# output
'2018-09-20T21: 10: 13.821Z'
```

#### `record.region`

```python
print(record.region)

# output
'us-east-1'
```

#### `record.request`

```python
print(record.request)

# output
{
    'sourceIPAddress': '172.20.133.36'
}
```

#### `record.response`

```python
print(record.response)

# output
{
    'x-amz-request-id': '6B859DD0CE613FAE',
    'x-amz-id-2': 'EXLMfc9aiXZFzNwLKXpw35iaVvl/DkEA6GtbuxjfmuLN3kLPL/aGoa7NMSwpl3m7ICAtNbjJX4w='
}
```

#### `record.configuration_id`

```python
print(record.configuration_id)

# output
{
    'x-amz-request-id': '6B859DD0CE613FAE',
    'x-amz-id-2': 'EXLMfc9aiXZFzNwLKXpw35iaVvl/DkEA6GtbuxjfmuLN3kLPL/aGoa7NMSwpl3m7ICAtNbjJX4w='
}
```

#### `record.object`

```python
print(record.object)

# output
{
    'key': 'user-1-prefs.json',
    'size': 17545,
    'eTag': 'b79ac2ef68c08fa9ac6013d53038a26c',
    'sequencer': '005BA40CB5BD42013A'
}
```

#### `record.bucket`

```python
print(record.bucket)

# output
{
    'name': 'user-preferences',
    'ownerIdentity': {
        'principalId': 'A32KFL0DQ3MH8X'
    },
    'arn': 'arn:aws:s3:::user-preferences'
}
```

#### `record.bucket_arn`

```python
print(record.bucket_arn)

# output
'arn:aws:s3:::user-preferences'
```

#### `record.bucket_owner`

```python
print(record.bucket_owner)

# output
'A32KFL0DQ3MH8X'
```

#### `record.key`

```python
print(record.key)

# output
'user-1-prefs.json'
```

#### `record.schema_version`

```python
print(record.schema_version)

# output
'1.0'
```

#### `record.user_identity`

```python
print(record.user_identity)

# output
'AWS: AROAI7Z5ZQEQ3UETKKYGQ: deploy-workers-poc-put-v1-photo'
```

#### `record.operation`

```python
print(record.operation)

# output
'created'
```

#### `record.body`

```python
print(record.body)

# output
{
    'possible': 'output'
}
```
