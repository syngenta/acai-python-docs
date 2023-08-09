---
title: Quickstart
description: Use Acai with Kinesis Events
---

# Kinesis Quickstart

Event handler for Amazon Kinesis Stream Events.

## Features

* Automatically decode kinesis base 64 string into dict (or whatever the decode thing is)
* Able to validate Kinesis record against a JSON Schema
* Assign Data Classes to records instead of getting Kinesis JSON dicts

## Installation

=== "Shell"
```bash
$ pip install acai
# pipenv install acai
# poetry add acai
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.

=== "kinesis.py"

    ```python
    from acai.kinesis.requirements import requirements
    
    @requirements()
    def handle(event):
        for record in event.records:
            print(record)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        kinesis-handler:
            handler: service/handlers/Kinesis.handle
            memorySize: 512
            timeout: 30
            events:
                - stream:
                    type: Kinesis
                    arn:
                      Fn::GetAtt: [ MyKinesisStream, Arn ]
    ```
