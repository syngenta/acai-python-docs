---
title: Quickstart
description: Use Acai with Firehose Events
---

# Firehose Quickstart

Event handler for Amazon firehose Stream Events.

## Features

* Automatically decode firehose base 64 string into dict (or whatever the decode thing is)
* Able to validate firehose record against a JSON Schema
* Assign Data Classes to records instead of getting firehose JSON dicts

## Installation

=== "Shell"
```bash
$ pip install acai
# pipenv install acai
# poetry add acai
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.

=== "firehose.py"

    ```python
    from acai.firehose.requirements import requirements
    
    @requirements()
    def handle(event):
        for record in event.records:
            print(record)
    ```

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
                      Fn::GetAtt: [ MyFirehoseStream, Arn ]
    ```
