---
title: Configuration Details
description: Advance usage and understanding of the Acai with Apigateway
---

# Apigateway Configuration Details

The router is will automatically route based structure of your files. 
There is no need to manage lists of routes matched to files or exports; all that is
required is that you create a file in the location or pattern configured to hold your endpoints and the router will
automatically find it.

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/apigateway) which can run locally! 
    :nerd:

## Lambda Configuration

=== "Serverless Configuration"

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

=== "Handler Configuration"

    ```py
    from acai_aws.apigateway.router import Router

    router = Router(
        base_path='your-service/v1',
        handlers='api/handlers',
        schema='api/openapi.yml',
        cors=True, # default True
        auto_validate=True, # default False
        validate_response=True, # default False
        verbose_logging=True, # default False
        timeout=25, # time in seconds, ints only,
        output_error=False, # default True;
        cache_mode='all', # static-only | dynamic-only ; all is default
        cache_size=512, # 128 is default; use None to disable cache
        before_all=before_all_example,
        after_all=after_all_example,
        on_error=on_error_example,
        with_auth=with_auth_example,
        on_timeout=on_timeout_example
    )
    router.auto_load()

    def route(event, context):
        return router.route(event, context)
    

    # requirements = kwargs from @requirements decorator; default: {}
    def before_all_example(request, response, requirements): 
        pass


    # requirements = kwargs from @requirements decorator; default: {}
    def after_all_example(request, response, requirements):
        pass


    # requirements = kwargs from @requirements decorator; default: {}
    def with_auth_example(request, response, requirements):
        pass


    # error is the exception object raised
    def on_error_example(request, response, error): 
        pass


    # error is the exception object raised
    def on_timeout_example(request, response, error): 
        pass

    ```

#### Router Configuration Details

| option                  | type | required                               | description                                                                                                                                       |
|-------------------------|------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| **`after_all`**         | func | no                                     | will call this function after EVERY request to the API                                                                                            |
| **`auto_validate`**     | bool | no; requires `schema`                  | will automatically validate request against openapi.yml                                                                                           |
| **`base_path`**         | str  | yes                                    | the base path of the API Gateway instance this is running on                                                                                      |
| **`before_all`**        | func | no                                     | will call this function before EVERY request to the API                                                                                           |
| **`cache_mode`**        | str  | no; 'all','static-only','dynamic-only' | will cache route endpoint module (not response) based on option, all (default), static endpoints or dynamic endpoints (route with path variables) |
| **`cache_size`**        | int  | no; (default 128)                      | how many endpoint modules to cache                                                                                                                |
| **`handlers`**          | str  | yes                                    | file path pointing to the directory where the endpoints are                                                                                       |
| **`on_error`**          | func | no                                     | will call this function on every unhandled error; not including validation errors                                                                 |
| **`output_error`**      | bool | no (default: true)                     | will output more detailed error from stacktrace as part of api response; otherwise will only say `internal server error`                          |
| **`schema`**            | str  | yes, if `auto_validate`                | file path pointing to the location of the openapi.yml file                                                                                        |
| **`with_auth`**         | func | no                                     | will call this function when `requirements` decorator have `auth_required` set to `True`                                                          |
| **`validate_response`** | bool | no                                     | will validate response of an endpoint, can effect performance, not recommended for production                                                     |
| **`verbose_logging`**   | bool | no                                     | will log every setup, every request and every response                                                                                            |
| **`timeout`**           | int  | no (default `None`)                    | timeout functionality for main handler logic (does not indclude before, after, before_all, after_all)                                             |
| **`on_timeout`**        | func | no                                     | when timout error is raised, this function will run                                                                                               |
| **`cors`**              | bool | no (default True)                      | will open cors to allow hitting from any source (`*`)                                                                                             |


## Routing Options

There are three ways to organize your routes: `directory`, `pattern` and `mapping`; `directory` and `pattern` routing 
mode requires your project files to be placed in a particular way; `mapping` does not require any structure, as you 
define every route, and it's a corresponding file. Below are the three ways configure your router:

#### Routing Mode: Directory

???+ tip
    If you are using route params, you will need use dynamic file names which requires it begins with an `_`. 
    
    example: `_some_variable_name.py`.

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

=== "router.py"

    ```py
    from acai_aws.apigateway.router import Router
    
    router = Router(
        base_path='your-service/v1',
        handlers='api/*_handler.py',
        schema='api/openapi.yml'
    )
    router.auto_load()
    
    def handle(event, context):
        return router.route(event, context)
    ```

#### Routing Mode: Mapping

???+ tip
    It may be more maintainable to store your routes list in a separate file, this example does not have that for brevity

???+ warning
    Even though you are matching your files to your routes, the handler files must have functions that match HTTP method (see endpoint examples [here](/acai-python-docs/apigateway/configuration-details/#endpoint-configuration-options))

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
    from acai_aws.apigateway.router import Router
    
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

## Endpoint Configuration Options

Each endpoint is meant to be treated as a separate module within the API. These endpoints are not meant to be extended 
or commingled and thus should approach individually. If resources are meant to be shared across endpoints, then 
those resources should be packaged as shared classes or utilities.

Every endpoint file should contain a function which matches an 
[HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) in lower case. 
Most common are `post`, `get`, `put`, `patch`, `delete`, but this library does support custom methods, 
if you so choose. As long as the method of the request matches the function name, it will work.

Each method within the endpoint file can have individual validation requirements. These requirements allow you to test 
all structural points of the request, with the ability to use JSONSchema and custom middleware to further extend the 
validation options.

???+ info
    See the full configuration list, explanation and example of each setting in our 
    [Configurations Section](/acai-python-docs/apigateway/endpoint/configurations/).

???+ tip
    If you are already using an `openapi.yml`, none of these requirements below are necessary. Ensure your `router` has 
    enabled [`auto_validate`](/acai-python-docs/apigateway/router/configurations/#example-router-config-with-directory-routing) 
    with proper `schema` configured and the below requirements are not necessary for any basic structural validation 
    (headers, body, query, params will be checked via openapi.yml). You can still use `before`, `after` & `data_class` with 
    other custom validations for more advanced use cases.

```python
# example for endpoint file: api/grower.py
from acai_aws.apigateway.requirements import requirements
from acai_aws.common.logger import logger

from api.logic.grower import Grower
from api.logic.middlware import log_grower, filter_grower


# example after function
def filter_grower(request, response, requirements):
    if 'GET' in response.raw['message']:
      logger.log(log=response.raw)
    
@requirements(
    required_query=['requester_id'],
    available_query=['grower_id', 'grower_email'],
    data_class=Grower,
    after=filter_grower,
    auth_required=True
)
def get(request, response):
    response.body = {'message': 'GET called', 'request_query_params': request.query_params}
    return response


# example before function
def log_grower(request, response, requirements):
    logger.log(log=request.body['grower_id'])
    
@requirements(
    required_body='v1-grower-post-request',
    before=log_grower,
    auth_required=True
)
def post(request, response):
    response.body = {'message': 'POST called', 'request_body': request.body}
    return response


@requirements(
    required_headers=['x-api-key', 'x-correlation-id']
    required_route='grower/{grower_id}'
    auth_required=True
    required_body={
        'type': 'object',
        'required': ['grower_id'],
        'additionalProperties': False,
        'properties': {
            'grower_id': {
                'type': 'string'
            },
            'body': {
                'type': 'object'
            },
            'dict': {
                'type': 'boolean'
            }
        }
    }
)
def patch(request, response):
    response.body = {'message': 'PATCH called', 'request_body': request.body}
    return response


@requirements(timeout=20) # this will override timeout set in router.py
def put(request, response):
    response.body = {'message': 'PUT called'}
    return response


# requirements is not required
def delete(request, response):
    response.body = {'message': 'DELETE called'}
    return response
```


### Full Requirements Configuration Options

| requirement                                                                                      | type  | description                                                           |
|--------------------------------------------------------------------------------------------------|-------|-----------------------------------------------------------------------|
| **[`required_headers`](/acai-python-docs/apigateway/configuration-details/#required_headers)**   | array | every header in this array must be in the headers of request          |
| **[`available_headers`](/acai-python-docs/apigateway/configuration-details/#available_headers)** | array | only headers in this array will be allowed in the request             |
| **[`required_query`](/acai-python-docs/apigateway/configuration-details/#required_query)**       | array | every item in the array is a required query string parameter          |
| **[`available_query`](/acai-python-docs/apigateway/configuration-details/#available_query)**     | array | only items in this array are allowed in the request                   |
| **[`required_route`](/acai-python-docs/apigateway/configuration-details/#required_route)**       | str   | when using parameters, this is the required parameters                |
| **[`required_body`](/acai-python-docs/apigateway/configuration-details/#required_body)**         | str   | references a JSschema component in your `schema`                      |
| **[`required_response`](/acai-python-docs/apigateway/configuration-details/#required_response)** | str   | references a JSschema component in your `schema` to validate response |
| **[`required_auth`](/acai-python-docs/apigateway/configuration-details/#auth_required)**         | bool  | will trigger `with_auth` function defined in the router config        |
| **[`before`](/acai-python-docs/apigateway/configuration-details/#before)**                       | func  | a custom function to be ran before your method function               |
| **[`after`](/acai-python-docs/apigateway/configuration-details/#after)**                         | func  | a custom function to be ran after your method function                |
| **[`data_class`](/acai-python-docs/apigateway/configuration-details/#data_class)**               | class | a custom class that will be passed instead of the request obj         |
| **[`timeout`](/acai-python-docs/apigateway/configuration-details/#timeout)**                     | bool  | timeout set for that method, not including before/after calls         |
| **[`summary`](/acai-python-docs/apigateway/configuration-details/#summary)**                     | str   | summary for use with openapi doc generation                           |
| **[`deprecated`](/acai-python-docs/apigateway/configuration-details/#deprecated)**               | bool  | deprecated for use with openapi doc generation                        |
| **[`custom-requirement`]**                                                                       | any   | see bottom of section                                                 |

#### `required_headers`

???+ info
    Headers are case-sensitive, make sure your casing matches your expectations.

```python
@requirements(
    required_headers=['x-api-key']
)
def post(request, response):
    pass
```

#### `available_headers`

???+ warning
    This is not recommended for frequent use as it raises errors for every header which does not conform to the array provided. Many browsers, http tools, and libraries will automatically add headers to request, unbeknownst to the user. By using this setting, you will force every user of the endpoint to take extra care with the headers provided and may result in poor API consumer experience.

```python
@requirements(
    available_headers=['x-api-key', 'x-on-behalf-of']
)
def post(request, response):
    pass
```

#### `required_query`

```python
@requirements(
    required_query=['grower_id']
)
def get(request, response):
    pass
```

#### `available_query`
???+ info
    `available_query` entries do NOT need to include entries already defined in the `required_query`; what is required,is assumed to be available.

```python
@requirements(
    available_query=['grower_email']
)
def get(request, response):
    pass
```

#### `required_route`

???+ warning
    This is required if you are using dynamic routing (ex. `_id.py`) with path parameters. The router will provide a path values in `request.path_params`

```python
@requirements(
    required_route='grower/{id}'
)
def get(request, response):
    pass
```

#### `required_body`

???+ info
    This is referencing a `components.schemas` section of your openapi.yml file defined in the `schema` value in your router config, but you can also pass in a `json schema` in the form of a `dict`.

```python
@requirements(
    required_body='v1-grower-post-request'
)
def post(request, response):
    pass


@requirements(
    required_body={
        'type': 'object',
        'required': ['grower_id'],
        'additionalProperties': False,
        'properties': {
            'grower_id': {
                'type': 'string'
            },
            'body': {
                'type': 'object'
            },
            'dict': {
                'type': 'boolean'
            }
        }
    }
)
def patch(request, response):
    pass
```

#### `required_response`

???+ info
    This is referencing a `components.schemas` section of your openapi.yml file defined in the `schema` value in your router config, but you can also pass in a `json schema` in the form of a `dict`.

```python
@requirements(
    required_response='v1-grower-post-response'
)
def post(request, response):
    pass


@requirements(
    required_response={
        'type': 'object',
        'required': ['grower_id'],
        'additionalProperties': False,
        'properties': {
            'grower_id': {
                'type': 'string'
            },
            'body': {
                'type': 'object'
            },
            'dict': {
                'type': 'boolean'
            }
        }
    }
)
def patch(request, response):
    pass
```


#### `auth_required`

???+ info
    This will trigger the function you provided in the router config under the `with_auth` configuration

```python
@requirements(
    auth_required=True
)
def delete(request, response):
    pass
```

#### `before`

```python
def before_func(request, response, requirements):
    print(request)
    print(response)
    print(requirements)

    
@requirements(
    before=before_func
)
def post(request, response):
    pass
```

#### `after`

```python
def after_func(request, response, requirements):
    print(request)
    print(response)
    print(requirements)

    
@requirements(
    before=after_func
)
def post(request, response):
    pass
```

#### `data_class`

???+ info
    Instead of getting a `request` and `response` as arguments passed to your API function, you will get an instance 
of the class you provided here

```python
class Grower:
    def __init__(self, request):
        for k, v in request.body.items():
            setattr(self, k, v)

@requirements(
    data_class=Grower
)
def post(grower, response):
    pass
```

#### `timeout`

???+ info
    This will override the timeout set in the main router configuration and only counts time for this request, not including before/after functions

```python

@requirements(timeout=20)
def post(grower, response):
    pass
```

#### custom requirements

???+ info
    You can add as many custom requirements as you want, with any variable type you want, and they will be passed to 
    your `before_all`, `before`, `after_all`, `after` and `with_auth` middleware defined functions.

```python
@requirements(
    your_custom_requirement={'whatever': ('you', 'want')}
)
def put(request, response):
    pass
```

#### `summary`

???+ info
    This is ONLY useful with openapi doc generation

```python

@requirements(summary='some summary about what this endpoint does')
def post(grower, response):
    pass
```

#### `deprecated`

???+ info
    This is ONLY useful with openapi doc generation

```python

@requirements(deprecated=True)
def post(grower, response):
    pass
```


## Request Object

By default, every endpoint function will receive an instance of the `Request` class (aka `request`) as the first 
argument of their function. This `request` has a lot of properties which will do common things automatically, but 
still allows the developer to override those operations if they deem necessary. Below is a list and examples of all 
the properties of the `request`:

### Request Properties

| property                                                                            |  type  | mutable | description                                                   |
|:------------------------------------------------------------------------------------|:------:|:-------:|:--------------------------------------------------------------|
| [`method`](/acai-python-docs/apigateway/configuration-details/#requestmethod)             |  str   |   no    | the http method of the request                                |
| [`cookies`](/acai-python-docs/apigateway/configuration-details/#requestcookies)           |  list  |   no    | the cookies of the request                                    |
| [`protocol`](/acai-python-docs/apigateway/configuration-details/#requestprotocol)         |  str   |   no    | the protocol of the request                                   |
| [`content_type`](/acai-python-docs/apigateway/configuration-details/#requestcontent_type) |  str   |   no    | the content_type of the request body                          |
| [`host_url`](/acai-python-docs/apigateway/configuration-details/#requesthost_url)         |  str   |   no    | the host_url of the request was sent to                       |
| [`domain`](/acai-python-docs/apigateway/configuration-details/#requestdomain)             |  str   |   no    | the domain of the request was sent to                         |
| [`stage`](/acai-python-docs/apigateway/configuration-details/#requeststage)               |  str   |   no    | the stage the lambda was deployed to                          |
| [`resource`](/acai-python-docs/apigateway/configuration-details/#requestresource)         |  str   |   no    | the AWS resource being invoked                                |
| [`authorizer`](/acai-python-docs/apigateway/configuration-details/#requestauthorizer)     | object |   no    | if using a customized authorizer, the authorizer object       |
| [`headers`](/acai-python-docs/apigateway/configuration-details/#requestheaders)           | object |   no    | the headers of the request                                    |
| [`params`](/acai-python-docs/apigateway/configuration-details/#requestparams)             | object |   no    | combination of query string and path params in one object     |
| [`query_params`](/acai-python-docs/apigateway/configuration-details/#requestquery_params) | object |   no    | query string parameters from the request                      |
| [`path_params`](/acai-python-docs/apigateway/configuration-details/#requestpath_params)   | object |   no    | the path parameters of the request                            |
| [`route`](/acai-python-docs/apigateway/configuration-details/#requestroute)               |  str   |   no    | the requested route with placeholders of params               |
| [`path`](/acai-python-docs/apigateway/configuration-details/#requestpath)                 |  str   |   no    | the raw requested path with actual param values               |
| [`json`](/acai-python-docs/apigateway/configuration-details/#requestjson)                 | object |   no    | the body of the request, converted from json string in object |
| [`xml`](/acai-python-docs/apigateway/configuration-details/#requestxml)                   | object |   no    | the body of the request, converted from xml string in object  |
| [`graphql`](/acai-python-docs/apigateway/configuration-details/#requestgraphql)           |  str   |   no    | the body of the graphql request as a string                   |
| [`body`](/acai-python-docs/apigateway/configuration-details/#requestbody)                 |  any   |   no    | the body of the request, converted to based on data type      |
| [`raw`](/acai-python-docs/apigateway/configuration-details/#requestraw)                   |  any   |   no    | the raw body of the request no conversion                     |
| [`context`](/acai-python-docs/apigateway/configuration-details/#requestcontext)           | object |   yes   | mutable request context to assigned and pass around           |
| [`event`](/acai-python-docs/apigateway/configuration-details/#requestevent)               | object |   no    | the full event originally coming from the lambda              |

#### `request.cookies`

```python
print(request.cookies)

# output: 
['some-cookie']
```

#### `request.protocol`

```python
print(request.protocol)

# output: 
'https'
```

#### `request.content_type`

```python
print(request.content_type)

# output: 
'application/json'
```

#### `request.host_url`

```python
print(request.host_url)

# output: 
'https://api.are-great.com'
```

#### `request.domain`

```python
print(request.domain)

# output: 
'api.are-great.com'
```

#### `request.stage`

```python
print(request.stage)

# output: 
'prod'
```

#### `request.method`

```python
print(request.method)

# output: 
'get'
```

#### `request.resource`

```python
print(request.resource)

# output: 
'/{proxy+}'
```

#### `request.authorizer`

???+ tip
    This is only useful if you are using an external authorizer with your lambda.

```python
print(request.authorizer)

# output:
{
    'apiKey': 'SOME KEY',
    'userId': 'x-1-3-4',
    'correlationId': 'abc12312',
    'principalId': '9de3f415a97e410386dbef146e88744e',
    'integrationLatency': 572
}
```

#### `request.headers`

```python
print(request.headers)

# output:
{
    'x-api-key': 'SOME-KEY',
    'content-type': 'application/json'
}
```

#### `request.params`

???+ info
    This combines both path parameters and query string parameters, nested in one object.

```python
print(request.params)

# output:
{
    'query': {
        'name': 'me'
    },
    'path': {
        'id': 1
    }
}
```

#### `request.query_params`

```python
print(request.query_params)

# output:
{
     'name': 'me'
}
```

#### `request.path_params`

```python

print(request.path_params)

# output:
{
     'id': 1
}
```

#### `request.route`

???+ info
    This will provide the route with the path param variables included

```python

print(request.route)

# output:
'grower/{id}'
```

#### `request.path`

???+ info
    This will provide the route with the path param values replacing the variables

```python
print(request.path)

# example output: 
'grower/1'
```

#### `request.json`

???+ warning
    This will raise an unhandled exception if the body is not json compatible

```python

print(request.json);

# output:
{
    'some_json_key': 'some_json_value'
}
```

```python

print(request.form);

# output:
{
    'some_form_key': 'some_form_value'
}
```

#### `request.xml`

???+ warning
    This will raise an unhandled exception if the body is not xml compatible

```python
python(request.xml);

# output:
{
    'some_xml_key': 'some_xml_value'
}
```


#### `request.graphql`

???+ info
    This is graphql string since there is no object equivalent; you can pass this directly to your graphql resolver

```python

python(request.graphql);

# output:
'{
    players {
        name
    }
}'
```

#### `request.body`

???+ tip
    This is the safest way to get the body of the request. It will use the `content-type` header to determine the data sent and convert it; if the data can't be converted for whatever reason it will catch the error and return the raw body provided unconverted.

```python

print(request.body)

# output:
{
    'some_key': 'some_value'
}
```


#### `request.raw`

```python

print(request.raw)

# output: 
# whatever the raw data of the body is; string, json string, xml, binary, etc
```


#### `request.context`

???+ tip
    This is the only mutable property of the request, to be used by any of the `before` or `before_all` middleware options

```python

request.context = {'application_assignable': true}
print(request.context)

# output:
{
    'application_assignable': true
}
```

#### `request.event`

???+ warning
    This is the original full request. Not advisable to use this as defeats the purpose of the entire Acai :smile:. In addition, you don't want to mutate this object and potentially mess up the entire router.

```python

print(request.event)

# output:
{
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/my/path",
    "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
    "cookies": [
        "cookie1",
        "cookie2"
    ],
    "headers": {
        "header1": "value1",
        "header2": "value1,value2"
    },
    "queryStringParameters": {
        "parameter1": "value1,value2",
        "parameter2": "value"
    },
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "api-id",
        "authentication": {
            "clientCert": {
                "clientCertPem": "CERT_CONTENT",
                "subjectDN": "www.example.com",
                "issuerDN": "Example issuer",
                "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                "validity": {
                    "notBefore": "May 28 12:30:02 2019 GMT",
                    "notAfter": "Aug  5 09:36:04 2021 GMT"
                }
            }
        },
        "authorizer": {
            "jwt": {
                "claims": {
                    "claim1": "value1",
                    "claim2": "value2"
                },
                "scopes": [
                    "scope1",
                    "scope2"
                ]
            }
        },
        "domainName": "id.execute-api.us-east-1.amazonaws.com",
        "domainPrefix": "id",
        "http": {
            "method": "POST",
            "path": "/my/path",
            "protocol": "HTTP/1.1",
            "sourceIp": "IP",
            "userAgent": "agent"
        },
        "requestId": "id",
        "routeKey": "$default",
        "stage": "$default",
        "time": "12/Mar/2020:19:03:58 +0000",
        "timeEpoch": 1583348638390
    },
    "body": "Hello from Lambda",
    "pathParameters": {
        "parameter1": "value1"
    },
    "isBase64Encoded": False,
    "stageVariables": {
        "stageVariable1": "value1",
        "stageVariable2": "value2"
    }
}
```


## Response Object

By default, every endpoint function will receive an instance of the `Response` class (aka `response`) as the second argument of their function. 
This response object is meant to provide consistency to HTTP response codes and error signatures. Below is a list and examples of all the properties of the `response`:

### Response Properties

| property                                                                      | type    | description                                                   |
|-------------------------------------------------------------------------------|---------|---------------------------------------------------------------|
| [`headers`](/acai-python-docs/apigateway/configuration-details/#responseheaders)    | tuple   | provide headers in tuple pairs to add new headers             |
| [`code`](/acai-python-docs/apigateway/configuration-details/#responsecode)          | int     | http response code to be returned the requester               |
| [`body`](/acai-python-docs/apigateway/configuration-details/#responsebody)          | any     | body of the response automatically converted to JSON string   |
| [`raw`](/acai-python-docs/apigateway/configuration-details/#responserawbody)        | any     | body of the response not converted to JSON string             |
| [`compress`](/acai-python-docs/apigateway/configuration-details/#responsecompress)  | bool    | will compress the body if set to true and add proper headers  |
| [`set_error`](/acai-python-docs/apigateway/configuration-details/#responseseterror) | func    | function to set an error with a key and value                 |
| [`has_error`](/acai-python-docs/apigateway/configuration-details/#responsehaserror) | boolean | simple property to check if response already has errors in it |


#### `response.headers`

```python
response.headers = ('status', 'ok')
response.headers = ('response_id', 'some-guid')

print(response.headers)

# output:
{
    'status': 'ok',
    'response_id': 'some-guid',
}
```

#### `response.code`

```python
response.code = 418;

print(response.code);

# output:
418
```

#### `response.body`

???+ info
    This will automatically convert the body to json if possible when called.

```python
response.body = {'some_key': 'some_value'}

print(response.body)

# output:
'{"someKey":"someValue"}'
```

#### `response.raw`

???+ info
    This will NOT automatically convert the body to json if possible when called. This is great when working with an `after_all` method that wants to mutate the body of the response before returning to the user.

```python
response.raw = {'some_key': 'some_value'};

print(response.raw)

# output:
{
    'some_key': 'some_value'
}
```

#### `response.compress`

???+ info
    This will compress whatever is in the body property.

```python
response.compress = True

print(response.body)
# output: this will gzip and compress the body.
```

#### `response.set_error(key, value)`

```python
some_key = 'abc123'
response.set_error('someKey', f'{some_key} is not a valid key to use with this service; try again with a different key')
another_key = 'def456'
response.set_error('anotherKey', f'{another_key} is not the correct type to operate on')

print(response.raw)

# output:
{
    'errors': [
        {
            'key_path': 'someKey',
            'message': 'abc123 is not a valid key to use with this service; try again with a different key'
        },
        {
            'key_path': 'anotherKey',
            'message': 'def456 is not the correct type to operate on'
        }
    ]
}
```

#### `response.has_error`

```python
response.setError('user', 'your access is denied')
print(response.has_error)

# output:
True


response.body = {'user': 'you have been granted access'};
print(response.has_error)

# output:
False
```

## Generate OpenAPI Docs from Codebase

You can generate a openapi yaml and/or json doc from your existing codebase. This feature can also add to existing openapi docs and/or overwrite
incorrect documentation.

#### command

```shell
python -m acai_aws.apigateway generate-openapi --handlers=tests/mocks/apigateway/openapi/**/*.py --base=acai_aws/example --output=tests/outputs --format=json,yml --delete
```

#### output

```shell
STARTED
generating openapi docs...
validating arguments received...
arguments validated...
scanning handlers: tests/mocks/apigateway/openapi/**/*.py...
importing handler endpoint modules...
deleting paths and methods not found in code base
writing openapi doc to requested directory: tests/outputs
COMPLETED
```

#### options

```shell
--handlers (-l): directory or pattern location of your handlers
--base (-b): (optional) base path of the api url; default='/'
--output (-o): (optional) directory location to save openapi file; defaults handlers directory location
--format (-f): (optional) comma deliminted format options (yml, json)
--delete (-d): (optional) will delete routes and methods in existing openapi doc not found in code base
```
