---
title: Quickstart
description: Use Acai with SQS Events
---

# SNS Quickstart

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

=== "sns.py"

    ```python
    from acai.sns.requirements import requirements
    
    requirements(
        required_body='v1'-sns-event'
    )
    def handle(event):
        for record in event.records:
            print(record)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        sns-handler:
            handler: service/handlers/sns.handle
            memorySize: 512
            timeout: 900
            events:
                - sqs:
                    arn:
                        Fn::GetAtt: [ SomeTopic, 'Arn' ]
    ```
