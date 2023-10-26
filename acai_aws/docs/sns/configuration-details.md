---
title: Configurations
description: Configure SNS Acai Events
---

# SNS Event Configurations

The SNS event will automatically handle many common things done when eventing off an SNS stream. Developers 
then have the ability to further extend that functionality with custom middleware. Below is a full list of all the 
configurations available and examples of their use.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/sns) which can be deployed in 1 
    command into your AWS account! :nerd:

## Lambda Configuration

=== "Serverless Configuratin"

    ```yaml
    functions:
        sns-handler:
            handler: service/handlers/sns.handle
            memorySize: 512
            timeout: 900
            events:
                - sns:
                    arn:
                        Fn::GetAtt: [ SomeTopic, 'Arn' ]
    ```

=== "Handler Configuratin"

    ```python
    from acai_aws.sns.requirements import requirements
    from acai_aws.common import logger

    @requirements(
        before=log_something,
        data_class=SomeClass,
        raise_body_error=True,
        schema='service/openapi.yml',
        required_body='v1-sns-body', # or jsonschema dict
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

| option                 | type        | required | default                           | description                                                           |
|------------------------|-------------|----------|-----------------------------------|-----------------------------------------------------------------------|
| **`before`**           | func        | no       | None                              | a custom function to be ran before your records are pulled            |
| **`after`**            | func        | no       | None                              | a custom function to be ran after your records are pulled             |
| **`data_class`**       | class       | no       | None                              | a custom class that will be passed instead of the records object      |
| **`raise_body_error`** | bool        | no       | False                             | will raise exception if body of record does not match schema provided |
| **`required_body`**    | str or dict | no       | None                              | will validate body of record against this schema                      |
| **`schema`**           | str         | no       | None                              | file path pointing to the location of the openapi.yml file            |

## SNS Record Properties

| property                                                                                          | type     | description                                                                       |
|---------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------|
| **[`source`](/acai-python-docs/sns/configuration-details/#recordsource)**                         | str      | the source of the event                                                           |
| **[`source_arn`](/acai-python-docs/sns/configuration-details/#recordsource_arn)**                 | str      | the source arn of the event                                                       |
| **[`region`](/acai-python-docs/sns/configuration-details/#recordregion)**                         | str      | the region of the event                                                           |
| **[`body`](/acai-python-docs/sns/configuration-details/#recordbody)**                             | dict,str | the body of the sns message                                                       |
| **[`attributes`](/acai-python-docs/sns/configuration-details/#recordattributes)**                 | dict     | the attributes dict of the message attributes; easier than use message attributes |
| **[`message_attributes`](/acai-python-docs/sns/configuration-details/#recordmessage_attributes)** | dict     | the message attributes of the message                                             |
| **[`version`](/acai-python-docs/sns/configuration-details/#recordversion)**                       | str      | the version sns event                                                             |
| **[`subscription_arn`](/acai-python-docs/sns/configuration-details/#recordsubscription_arn)**     | str      | the subscription arn of the sns event                                             |
| **[`signature_version`](/acai-python-docs/sns/configuration-details/#recordsignature_version)**   | str      | the signature version of the sns event                                            |
| **[`timestamp`](/acai-python-docs/sns/configuration-details/#recordtimestamp)**                   | str      | the timestamp of the sns event                                                    |
| **[`signature`](/acai-python-docs/sns/configuration-details/#recordsignature)**                   | str      | the signature of the sns event                                                    |
| **[`signing_cert_url`](/acai-python-docs/sns/configuration-details/#recordsigning_cert_url)**     | str      | the signing cert url of the sns event                                             |
| **[`message_id`](/acai-python-docs/sns/configuration-details/#recordmessage_id)**                 | str      | the message id of the sns event                                                   |
| **[`message`](/acai-python-docs/sns/configuration-details/#recordmessage)**                       | str      | the message of the sns event                                                      |
| **[`sns_type`](/acai-python-docs/sns/configuration-details/#recordsns_type)**                     | str      | the type of the sns event                                                         |
| **[`unsubscribe_url`](/acai-python-docs/sns/configuration-details/#recordunsubscribe_url)**       | str      | the unsubscribe_url of the sns event                                              |
| **[`topic_arn`](/acai-python-docs/sns/configuration-details/#recordtopic_arn)**                   | str      | the topic arn of the sns event                                                    |
| **[`subject`](/acai-python-docs/sns/configuration-details/#recordsubject)**                       | str      | the subject of the sns event                                                      |

#### `record.source`

```python
print(record.source)

# output
'aws:sns'
```

#### `record.source_arn`

```python
print(record.source_arn)

# output
'arn:aws:sns:us-east-2:123456789012:my-queue'
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

#### `record.version`

```python
print(record.version)

# output
'1.0'
```

#### `record.subscription_arn`

```python
print(record.subscription_arn)

# output
'arn:aws:sns:us-east-1:123456789012:sns-lambda:21be56ed-a058-49f5-8c98-aedd2564c486'
```

#### `record.signature_version`

```python
print(record.signature_version)

# output
'1'
```

#### `record.timestamp`

```python
print(record.timestamp)

# output
'2019-01-02T12:45:07.000Z'
```

#### `record.signature`

```python
print(record.signature)

# output
'tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r=='
```

#### `record.signing_cert_url`

```python
print(record.signing_cert_url)

# output
'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem'
```

#### `record.signing_cert_url`

```python
print(record.signing_cert_url)

# output
'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem'
```

#### `record.message_id`

```python
print(record.message_id)

# output
'95df01b4-ee98-5cb9-9903-4c221d41eb5e'
```

#### `record.message`

```python
print(record.message)

# output
{
    'key': 'value'
}
```

#### `record.sns_type`

```python
print(record.sns_type)

# output
'Notification'
```

#### `record.unsubscribe_url`

```python
print(record.unsubscribe_url)

# output
'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:us-east-1:123456789012:test-lambda:21be56ed-a058-49f5-8c98-aedd2564c486'
```

#### `record.topic_arn`

```python
print(record.topic_arn)

# output
'arn:aws:sns:us-east-1:123456789012:sns-lambda'
```

#### `record.subject`

```python
print(record.subject)

# output
'TestInvoke'
```
