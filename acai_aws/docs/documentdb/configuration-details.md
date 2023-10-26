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

=== "Serverless Configuration"

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

=== "Handler Configuration"

    ```python
    from acai_aws.documentdb.requirements import requirements
    from acai_aws.common import logger

    @requirements(
        before=log_something,
        operations=['created', 'deleted', 'updated'],
        data_class=SomeClass,
        raise_operation_error=True,
        raise_body_error=True,
        schema='service/openapi.yml',
        required_body='v1-docdb-body', # or jsonschema dict
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

## DocumentDB Record Properties

| property                                                                                       | type   | description                                          |
|------------------------------------------------------------------------------------------------|--------|------------------------------------------------------|
| **[`event_id`](/acai-python-docs/documentdb/configuration-details/#recordevent_id)**           | string | id of the event                                      |
| **[`cluster_time`](/acai-python-docs/documentdb/configuration-details/#recordcluster_time)**   | string | time from the cluster of the event                   |
| **[`document_key`](/acai-python-docs/documentdb/configuration-details/#recorddocument_key)**   | string | key of the document which was triggered              |
| **[`full_document`](/acai-python-docs/documentdb/configuration-details/#recordfull_document)** | dict   | full document of what was triggered                  |
| **[`operation`](/acai-python-docs/documentdb/configuration-details/#recordoperation)**         | string | operation which triggered the event                  |
| **[`change_event`](/acai-python-docs/documentdb/configuration-details/#recordchange_event)**   | string | detailed mongo specific operation event name         |
| **[`body`](/acai-python-docs/documentdb/configuration-details/#recordbody)**                   | dict   | the new image of dynamodb record; created or updated |
| **[`db`](/acai-python-docs/documentdb/configuration-details/#recorddb)**                       | dict   | mongo database details                               |
| **[`collection`](/acai-python-docs/documentdb/configuration-details/#recordcollection)**       | dict   | mongo collections details                            |


#### `record.event_id`

```python
print(record.event_id);

# output
'0163eeb6e7000000090100000009000041e1'
```

#### `record.cluster_time`

```python
print(record.cluster_time);

# output
'2023-02-16T00:00:00Z'
```

#### `record.document_key`

```python
print(record.document_key);

# output
'63eeb6e7d418cd98afb1c1d7'
```

#### `record.full_document`

```python
print(record.full_document);

# output
{
    '_id': {
        '$oid': '63eeb6e7d418cd98afb1c1d7'
    },
    'lang': 'en-us',
    'sms': True,
    'email': True,
    'push': True
}
```

#### `record.operation`

```python
print(record.operation);

# output
'created'
```

#### `record.change_event`

```python
print(record.change_event);

# output
'insert'
```

#### `record.body`

```python
print(record.body);

# output
{
    'id': '63eeb6e7d418cd98afb1c1d7',
    'lang': 'en-us',
    'sms': True,
    'email': True,
    'push': True
}
```

#### `record.db`

```python
print(record.db);

# output
'test_collection'
```

#### `record.collection`

```python
print(record.collection);

# output
'test_database'
```

