---
title: Quickstart
description: Use Acai with DynamoDB Events
---

# DynamoDB Quickstart

Event handler for Amazon DynamoDB Stream Events.

## Features

* Automatically convert DynamoDB JSON dict to standard JSON dict
* Only run on certain DynamoDB operations; i.e. when items are created, updated or deleted
* Able to validate DynamoDB record against a JSON Schema
* Assign Data Classes to records instead of getting DynamoDB JSON dicts

## Installation

=== "Shell"
```bash
$ pip install acai_aws
# pipenv install acai_aws
# poetry add acai_aws
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.

=== "dynamodb.py"

    ```python
    from acai_aws.dynamodb.requirements import requirements
    
    @requirements(
        operations=['created', 'deleted']
    )
    def handle(event):
        for record in event.records:
            print(record)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        ddb-handler:
            handler: service/handlers/dynamodb.handle
            memorySize: 512
            timeout: 30
            events:
                - stream:
                    type: dynamodb
                    arn:
                      Fn::GetAtt: [ SomeDDBTable, StreamArn ]
    ```
