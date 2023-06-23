---
title: APIGateway
description: Use Acai with APIGateway
---

Event handler for Amazon APIGateway REST & GraphQL.

## Features

* Configurable router based on 3 common routing patterns
* Built-in request validation using standard OpenAPI schema
* Easily validate request in modular and declarative way without any additional code
* Able to easily extend with custom middleware at both app and per-endpoint levels
* Support for CORS, binary and Gzip compression

## Getting Started

After installation, create a handler file and configure the AWS lambda to use that file as its handler.
For the full set of configurations, please review the full list of configurations found router setup page.

=== "endpoint_router.py"

    ```python
    from acai.apigateway.router import Router
    
    router = Router(
        base_path='your-service/v1',
        handlers='service/handlers',
        schema='service/openapi.yml'
    )
    router.auto_load()
    
    def handle(event, context):
        return router.route(event, context)
    ```

=== "serverless.yml"

    ```yaml
    functions:
        apigateway-handler:
            handler: service/handlers/endpoint_router.handle
            events:
                - http:
                    path: /
                    method: ANY
                - http:
                    path: /{proxy+}
                    method: ANY    
    ```
