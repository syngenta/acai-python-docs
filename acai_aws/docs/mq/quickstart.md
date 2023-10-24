---
title: Quickstart
description: Use Acai with MQ Events
---

# MQ Quickstart

Event handler for Amazon MQ Events.

## Features

* Automatically decode base 64 string into dict (or whatever the decode thing is)
* Able to validate body of record against a JSON Schema
* Assign Data Classes to records instead of getting firehose JSON dicts

## Installation

=== "Shell"
```bash
$ pip install acai_aws
# pipenv install acai_aws
# poetry add acai_aws
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.

=== "mq.py"

    ```python
    from acai_aws.mq.requirements import requirements
    
    @requirements()
    def handle(event):
        for record in event.records:
            print(record.body)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        mq-handler:
            handler: service/handlers/mq.handle
            memorySize: 512
            timeout: 30
            events:
                - rabbitmq:
                    arn: arn:aws:mq:us-east-1:0000:broker:ExampleMQBroker:b-xxx-xxx
                    queue: queue-name
                    basicAuthArn: arn:aws:secretsmanager:us-east-1:01234567890:secret:MySecret
    ```
