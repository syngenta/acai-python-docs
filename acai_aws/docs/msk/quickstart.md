---
title: Quickstart
description: Use Acai with MSK Events
---

# MSK Quickstart

Event handler for Amazon MSK Events.

## Features

* Automatically decodes base 64 string into dict (or whatever the decode thing is)
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

=== "generic.py"

    ```python
    from acai_aws.msk.requirements import requirements
    
    @requirements()
    def handle(event):
        for record in event.records:
            print(record.body)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        msk-handler:
            handler: service/handlers/msk.handle
            memorySize: 512
            timeout: 30
            events:
                - msk:
                    arn: arn:aws:kafka:region:XXXXXX:cluster/MyCluster/xxxx-xxxxx-xxxx
                    topic: mytopic
    ```
