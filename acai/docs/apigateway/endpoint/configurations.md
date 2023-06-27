---
title: Configuration Options
description: How to use the built-in validation & custom middleware
---

# Endpoint Configurations

In order to encourage "Happy Path Programming" and make it easier for developers to validate request fully, the Acai 
comes with a host of built-in validations as well as the ability to extend with custom validations and middleware. 
See the full validation list here:

???+ examples
    Don't like reading documentation? Then look at 
    [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/apigateway) which can run locally! 
    :nerd:

### Validation Configurations

| requirement                                                                                  | type  | description                                                    |
|----------------------------------------------------------------------------------------------|-------|----------------------------------------------------------------|
| **[`required_headers`]({{web.url}}/apigateway/endpoint/configurations/#required_headers)**   | array | every header in this array must be in the headers of request   |
| **[`available_headers`]({{web.url}}/apigateway/endpoint/configurations/#available_headers)** | array | only headers in this array will be allowed in the request      |
| **[`required_query`]({{web.url}}/apigateway/endpoint/configurations/#required_query)**       | array | every item in the array is a required query string parameter   |
| **[`available_query`]({{web.url}}/apigateway/endpoint/configurations/#available_query)**     | array | only items in this array are allowed in the request            |
| **[`required_path`]({{web.url}}/apigateway/endpoint/configurations/#required_path)**         | str   | when using parameters, this is the required parameters         |
| **[`required_body`]({{web.url}}/apigateway/endpoint/configurations/#required_body)**         | str   | references a JSschema component in your `schema`               |
| **[`required_auth`]({{web.url}}/apigateway/endpoint/configurations/#auth_required)**         | bool  | will trigger `with_auth` function defined in the router config |
| **[`before`]({{web.url}}/apigateway/endpoint/configurations/#before)**                       | func  | a custom function to be ran before your method function        |
| **[`after`]({{web.url}}/apigateway/endpoint/configurations/#after)**                         | func  | a custom function to be ran after your method function         |
| **[`data_class`]({{web.url}}/apigateway/endpoint/configurations/#data_class)**               | class | a custom class that will be passed instead of the request obj  |
| **[`custom-requirement`]**                                                                   | any   | see bottom of page                                             |

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
    This is not recommended for frequent use as it raises errors for every header which does not conform to the array 
provided. Many browsers, http tools, and libraries will automatically add headers to request, unbeknownst to the user. 
By using this setting, you will force every user of the endpoint to take extra care with the headers provided and 
may result in poor API consumer experience.

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
    `available_query` entries do NOT need to include entries already defined in the `required_query`; what is required,
is assumed to be available.

```python
@requirements(
    available_query=['grower_email']
)
def get(request, response):
    pass
```

#### `required_path`

???+ warning
    This is required if you are using dynamic routing (ex. `_id.py`) with path parameters. 
The router will provide a path values in `request.path_params`

```python
@requirements(
    required_path='grower/{id}'
)
def get(request, response):
    pass
```

#### `required_body`

???+ info
    This is referencing a `components.schemas` section of your openapi.yml file defined in the `schema` value in your 
router config, but you can also pass in a `json schema` in the form of a `dict`.

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

#### custom requirements (example)

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
