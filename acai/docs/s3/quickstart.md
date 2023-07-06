---
title: Quickstart
description: Use Acai with S3 Events
---

# S3 Quickstart

Event handler for Amazon S3 Bucket Events.

## Features

* Automatically convert JSON files to JSON objects
* Automatically convert CSV files to JSON objects
* Only run on certain S3 operations, like on when items are created, updated or deleted
* Able to validate S3 record against a JSON Schema
* Assign Data Classes to records instead of getting raw S3 JSON objects

## Installation

=== "Shell"
```bash
$ pip install acai
# pipenv install acai
# poetry add acai
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.

=== "s3.py"

    ```python
    from acai.s3.requirements import requirements
    
    requirements(
        get_object=True,
        data_type='json'
    )
    def handle(event):
        for record in event.records:
            print(record)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        s3-handler:
            handler: service/handlers/s3.handle
            memorySize: 512
            timeout: 900
            events:
                - s3:
                    bucket: uploadsBucket
                    event: s3:ObjectCreated:*
    ```
