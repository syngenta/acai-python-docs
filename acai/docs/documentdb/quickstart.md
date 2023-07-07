---
title: Quickstart
description: Use Acai with DocumentDB Events
---

# DocumentDB Quickstart

Event handler for Amazon DocumentDB Stream Events.

## Features

* Automatically convert DocumentDB IDs to standard strings
* Only run on certain DocumentDB operations; i.e. when documents are created, updated or deleted
* Able to validate DocumentDB document against a JSON Schema
* Assign Data Classes to records instead of getting DocumentDB BJSON dicts

## Installation

=== "Shell"
```bash
$ pip install acai
# pipenv install acai
# poetry add acai
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.

=== "documentdb.py"

    ```python
    from acai.documentdb.requirements import requirements
    
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
        documentdb-handler:
            handler: service/handlers/documentdb.handle
            memorySize: 512
            timeout: 30
            events:
                - stream:
                    type: documentdb
                    arn:
                      Fn::GetAtt: [ SomeDocDBCluser, ClusterArn ]
    ```
