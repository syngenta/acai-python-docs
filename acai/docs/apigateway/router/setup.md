---
title: Set Up
description: How to use the Acai Router
---

# Router Set Up

The router is the core of the apigateway event handler and will automatically route based on the way your project is 
configured. Most of the time there is no need for managing lists of routes matched to files or exports; all that is
required is that you create a file in the location or pattern configured to hold your endpoints and the router will
automatically find it.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/apigateway) which can run locally! 
    :nerd:

### 1. Configure the Lambda

=== "Serverless Framework"

```yaml
functions:
    apigateway-handler:
        handler: api/handler/router.route
        events:
            - http:
                path: /
                method: ANY
            - http:
                path: /{proxy+}
                method: ANY    
```

### 2. Configure the Router

There are three ways to organize your routes: `directory`, `pattern` and `mapping`; `directory` and `pattern` routing 
mode requires your project files to be placed in a particular way; `mapping` does not require any structure, as you 
define every route and it's corresponding file. Below are the three ways configure your router:

#### Routing Mode: Directory

???+ tip
    If you are using route params, you will need use dynamic file names which follow this pattern: 
`_some_variable_name.py`.

=== "file structure"

    ```
    ~~ Directory ~~                     ~~ Route ~~
    ===================================================================
    📦api/                              |          
    │---📂handler                       |           
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

=== "router.py"

    ```py
    from acai.apigateway.router import Router
    
    router = Router(
        base_path='your-service/v1',
        handlers='api/handlers',
        schema='api/openapi.yml'
    )
    router.auto_load()
    
    def handle(event, context):
        return router.route(event, context)
    ```

#### Routing Mode: Pattern

???+ tip
    You can use any [glob](https://en.wikipedia.org/wiki/Glob_(programming)) pattern you like; common patterns are:

    * `/**/*_handler.py`

    * `/**/handler_*.py`

    * `/**/handler.py`

=== "file structure"

    ```
    ~~ Pattern ~~                               ~~ Route ~~
    ================================================================================
    📦api/                                      |
    │---📜router.py                             |
    │---📂org                                   |
        │---📜org_handler.py                    | /org
        │---📜org_model.py                      |
        │---📜org_factory.py                    |
        │---📜org_logic.py                      |
    │---📂grower                                |
        │---📜grower_handler.py                 | /grower
        │---📜_grower_id_handler.py             | /grower/{grower_id}
        │---📜grower_model.py                   |
        │---📜grower_factory.py                 |
        │---📜grower_logic.py                   |
    │---📂farm                                  |
        │---📜farm_handler.py                   | /farm
        │---📜farm_logic.py                     |
        │---📜farm_model.py                     |
        │---📂_farm_id                          |
            │---📜_farm_id_handler.py           | /farm/{farm_id}
            │---📂field                         |
                │---📜field_handler.py          | /farm/{farm_id}/field
                │---📜_field_id_controller.py   | /farm/{farm_id}/field/{field_id}
                │---📜field_logic.py            |
                │---📜field_model.py            |
    ```

=== "router.jy"

    ```py
    from acai.apigateway.router import Router
    
    router = Router(
        base_path='your-service/v1',
        handlers='api/*_handler.py',
        schema='api/openapi.yml'
    )
    router.auto_load()
    
    def handle(event, context):
        return router.route(event, context)
    ```

#### Routing Mode: List

???+ tip
    It may be more maintainable to store your routes list in a separate file, this example does not have that for brevity

???+ warning
    Even though you are matching your files to your routes, the handler files must have functions that match HTTP method (see endpoint examples here)

???+ danger
    This is not the preferred routing mode to use; this can lead to a sloppy, unpredictable project architecture which will be hard to maintain and extend. This is *NOT RECOMMENDED*.

=== "file structure"

    ```
    File structure doesn't matter
    ======================================================
    📦api/
    │---📜router.py
    ```

=== "router.py"

    ```py
    from acai.apigateway.router import Router
    
    router = Router(
        base_path='your-service/v1',
        schema='api/openapi.yml'
        handlers={
            'grower': 'api/routes/grower.py',
            'farm': 'api/routes/farm.py',
            'farm/{farm_id}/field/{field_id}': 'api/routes/farm_field.py'
        }
    )
    router.auto_load()
    
    def handle(event, context):
        return router.route(event, context)
    ```


### 3. Configure the Endpoint File

Every endpoint file should contain a function which matches an 
[HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) in lower case. 
Most common are `post`, `get`, `put`, `patch`, `delete`, but this library does support custom methods, 
if you so choose. As long as the method of the request matches the function name, it will work.

```python
# example for endpoint file: api/grower.py
from acai.apigateway.requirements import requirements

from service.logic.grower import Grower
from service.logic.middlware import log_grower, filter_grower


@requirements(
    required_body='v1-grower-post-request',
    before=log_grower,
    auth_required=True
)
def post(request, response):
    response.body = {'message': 'POST called', 'request_body': request.body}
    return response


@requirements(
    required_query=['requester_id'],
    available_query=['grower_id', 'grower_email'],
    data_class=Grower,
    before=filter_grower,
    auth_required=True
)
def get(grower, response):
    response.body = {'message': 'GET called', 'grower': grower.to_dict()}
    return response

@requirements(
    required_header=['x-grower-id'],
    data_class=Grower,
    auth_required=True
)
def patch(grower, response):
    response.body = {'message': 'PATCH called', 'grower': grower.to_dict()}
    return response

@requirements(
    required_path='grower/{grower_id}',
    auth_required=True
)
def delete(request, response):
    response.body = {'message': 'DELETE called', 'request': request.path_params['grower_id']}
    return response
```
