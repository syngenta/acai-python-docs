---
title: Quickstart
description: Use Acai with SQS Events
---

# SQS Quickstart

Event handler for Amazon SQS Events.

## Features

* Automatically convert JSON from message body
* Automatically flatten message attributes
* Able to message body against a JSON Schema
* Assign Data Classes to records instead of getting record objects

## Installation

=== "Shell"
```bash
$ pip install acai
# pipenv install acai
# poetry add acai
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.

=== "sqs.py"

    ```python
    from acai.sqs.requirements import requirements
    
    @requirements(
        required_body='v1'-sqs-event'
    )
    def handle(event):
        for record in event.records:
            print(record)
    ```

=== "serverless.yml"

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
