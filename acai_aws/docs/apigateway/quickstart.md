---
title: Quickstart
description: Use Acai with APIGateway
---

# Apigateway Quickstart

Event handler and router for Amazon APIGateway REST & GraphQL, allowing you to take advantage of procesing all api 
requests in one lambda.

## Features

* Configurable router based on 3 common routing patterns
* Built-in request validation using standard OpenAPI schema
* Easily validate request in modular and declarative way without any additional code
* Able to easily extend with custom middleware at both app and per-endpoint levels
* Support for CORS, binary and Gzip compression


## Installation
=== "Shell"
```bash
$ pip install acai_aws
# pipenv install acai_aws
# poetry add acai_aws
```

## Minimal Setup

After installation, create a handler file and configure the AWS lambda to use that file as its handler.
For the full set of configurations, please review the full list of configurations found router setup page.

=== "router.py"

    ```python
    from acai_aws.apigateway.router import Router
    
    router = Router(
        base_path='your-service/v1',
        handlers='api/handlers',
        schema='api/openapi.yml'
    )
    router.auto_load()
    
    def handle(event, context):
        return router.route(event, context)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        apigateway-handler:
            handler: api/handlers/router.handle
            events:
                - http:
                    path: /
                    method: ANY
                - http:
                    path: /{proxy+}
                    method: ANY    
    ```

=== "file structure"

    ```
    ~~ Directory ~~                     ~~ Route ~~
    ===================================================================
    📦api/                              |          
    │---📂handlers                      |           
        │---📜router.py                 |
        │---📜org.py                    | /org    
        │---📂grower                    |
            │---📜__init__.py           | /grower
            │---📜_grower_id.py         | /grower/{grower_id}
        │---📂farm                      |
            │---📜__init__.py           | /farm
            │---📂_farm_id              |
                │---📜__init__.py       | /farm/{farm_id}
                │---📂field             |
                    │---📜__init__.py   | /farm/{farm_id}/field
                    │---📜_field_id.py  | /farm/{farm_id}/field/{field_id}
    ```
