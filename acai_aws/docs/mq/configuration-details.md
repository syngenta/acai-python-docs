---
title: Configurations Details
description: Configure MQ Acai Events
---

# MQ Configurations Details

The mq event will automatically handle many common things done when eventing off a generic event invoked manually or programmatically. 
Developers then have the ability to further extend that functionality with custom middleware. 
Below is a full list of all the configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/mq) which can be deployed 
    in 1 command into your AWS account! :nerd:

## Lambda Configuration

=== "Serverless Configuration"

    ```yaml
    functions:
        generic-handler:
            handler: service/handlers/mq.handle
            memorySize: 512
            timeout: 30
            events:
                - rabbitmq:
                    arn: arn:aws:mq:us-east-1:0000:broker:ExampleMQBroker:b-xxx-xxx
                    queue: queue-name
                    basicAuthArn: arn:aws:secretsmanager:us-east-1:01234567890:secret:MySecret
    ```

=== "Handler Configuration"

    ```python
    from acai_aws.firehose.requirements import requirements
    from acai_aws.common import logger

    @requirements(
        before=log_something,
        data_class=SomeClass,
        raise_operation_error=True,
        raise_body_error=True,
        schema='service/openapi.yml',
        required_body='v1-mq-body', # or send jsonschema dict; schema kwarg not needed if sending jsonschema dict
        after=alert_something,
    )
    def handle(event):
        for record in event.records:
            logger.log(log=record.body)

    # example data class
    class SomeClass:
        def __init__(self, record):
            for k, v in record.body.items():
                setattr(self, k, v)

    # example before function
    def log_something(records, requirements):
        logger.log(log=event.body) 

    # example after function
    def alert_something(event, result, requirements):
        if 'something' in result and 'alert' in requirements:
            logger.log(log=event)
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

## MQ Event Properties

| property                                                                     | type             | description                                          |
|------------------------------------------------------------------------------|------------------|------------------------------------------------------|
| **[`message_id`](/acai-python-docs/mq/configuration-details/#recordmessage_id)**                   | str              | id of the message                                    |
| **[`message_type`](/acai-python-docs/mq/configuration-details/#recordmessage_type)**               | str              | type of the message                                  |
| **[`delivery_mode`](/acai-python-docs/mq/configuration-details/#recorddelivery_mode)**             | int              | mode of delivery                                     |
| **[`reply_to`](/acai-python-docs/mq/configuration-details/#recordreply_to)**                       | str (nullable)   | reply to string                                      |
| **[`record_type`](/acai-python-docs/mq/configuration-details/#recordrecord_type)**                 | str (nullable)   | type of record                                       |
| **[`expiration`](/acai-python-docs/mq/configuration-details/#recordexpiration)**                   | str              | expiration of message                                |
| **[`priority`](/acai-python-docs/mq/configuration-details/#recordpriority)**                       | int              | priority of message                                  |
| **[`correlation_id`](/acai-python-docs/mq/configuration-details/#recordcorrelation_id)**           | str              | correlation id of message                            |
| **[`redelivered`](/acai-python-docs/mq/configuration-details/#recordredelivered)**                 | bool             | whether the message has been redelivered             |
| **[`destination`](/acai-python-docs/mq/configuration-details/#recorddestination)**                 | dict             | destination of the message                           |
| **[`properties`](/acai-python-docs/mq/configuration-details/#recordproperties)**                   | dict             | properties of the message                            |
| **[`time_stamp`](/acai-python-docs/mq/configuration-details/#recordtime_stamp)**                   | int              | time_stamp of the message                            |
| **[`in_time`](/acai-python-docs/mq/configuration-details/#recordin_time)**                         | int              | in time of the message                               |
| **[`out_time`](/acai-python-docs/mq/configuration-details/#recordout_time)**                       | int              | out time of the message                              |
| **[`body`](/acai-python-docs/mq/configuration-details/#recordbody)**                               | any              | body of the message                                  |
| **[`data`](/acai-python-docs/mq/configuration-details/#recorddata)**                               | any              | data of the message                                  |


#### `record.message_id`

```python
print(record.message_id);

# output
'ID:b-9bcfa592-423a-4942-879d-eb284b418fc8-1.mq.us-west-2.amazonaws.com-37557-1234520418293-4:1:1:1:1'
```

#### `record.message_type`

```python
print(record.message_type);

# output
'jms/text-message'
```

#### `record.delivery_mode`

```python
print(record.delivery_mode);

# output
1
```

#### `record.reply_to`

```python
print(record.reply_to);

# output
None
```

#### `record.record_type`

```python
print(record.record_type);

# output
None
```

#### `record.expiration`

```python
print(record.expiration);

# output
'60000'
```

#### `record.priority`

```python
print(record.priority);

# output
1
```

#### `record.correlation_id`

```python
print(record.correlation_id);

# output
'myJMSCoID'
```

#### `record.redelivered`

```python
print(record.redelivered);

# output
False
```

#### `record.destination`

```python
print(record.destination);

# output
{
    'physicalName': 'testQueue'
}
```

#### `record.properties`

```python
print(record.properties);

# output
{
    'index': '1',
    'doAlarm': 'false',
    'myCustomProperty': 'value'
}
```

#### `record.time_stamp`

```python
print(record.time_stamp);

# output
1598827811958
```

#### `record.in_time`

```python
print(record.in_time);

# output
1598827811958
```

#### `record.out_time`

```python
print(record.out_time);

# output
1598827811959
```

#### `record.body`

```python
print(record.body);

# output
{
    'new_data': '123456789'
}
```

#### `record.data`

```python
print(record.data);

# output
{
    'new_data': '123456789'
}
```

