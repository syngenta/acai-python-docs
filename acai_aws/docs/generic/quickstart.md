---
title: Quickstart
description: Use Acai with Generic (AWS Console or CLI) Events
---

# Generic (AWS Console or CLI) Quickstart

Event handler for Amazon generic (AWS Console or CLI) Events.

## Features

* Automatically convert body into dict
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
    from acai_aws.generic.requirements import requirements
    
    @requirements()
    def handle(event):
        print(event.body)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        generic-handler:
            handler: service/handlers/generic.handle
            memorySize: 512
            timeout: 30
    ```
