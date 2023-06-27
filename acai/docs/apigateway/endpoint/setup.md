---
title: Set Up
description: How to set up an endpoint with Acai
---

# Endpoint Set Up

Each endpoint is meant to be treated as a separate module within the API. These endpoints are not meant to be extended 
or commingled and thus should approach individually. If resources are meant to be shared across endpoints, then 
those resources should be packaged as shared classes or utilities.

Each endpoint should read as a procedural list of steps to be completed. To help keep this list clean and easy to read, 
the Acai follows the philosophy of "Happy Path Programming." To achieve this, Acai comes with a plethora of 
validation configurations with the ability to extend with even more customized validation options. This ensures 
the request sent to your endpoint will be correct with little need for exception handling or complex conditionals.

???+ examples
    Don't like reading documentation? Then look at [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/apigateway) which can run locally! :nerd:

### 1. Match Function to HTTP Method

Each endpoint must have stateless functions which match the name of the HTTP method. 
If endpoint is called the a `POST` HTTP method, then the `post` endpoint function is invoked.

```python
# example for endpoint file: api/grower.py
def post(request, response):
    if request.body['user_type'] == 'grower':
        response.body = {'message': 'welcome grower!'}
    else:
        response.body = {'message': 'welcome other type of user'}
    return response
```

### 2. Configure the Requirements (optional)

Each method within the endpoint file can have individual validation requirements. These requirements allow you to test 
all structural points of the request, with the ability to use JSONSchema and custom middleware to further extend the 
validation options. Below is an example of a full requirements object:

???+ info
    See the full configuration list, explanation and example of each setting in our 
[Configurations Section]({{web.url}}/apigateway/endpoint/configurations/).

???+ tip
    If you are already using an `openapi.yml`, none of these requirements below are necessary. Ensure your `router` has 
enabled [`auto_validate`]({{web.url}}/apigateway/router/configurations/#example-router-config-with-directory-routing) 
with proper `schema` configured and the below requirements are not necessary for any basic structural validation 
(headers, body, query, params will be checked via openapi.yml). You can still use `before`, `after` & `data_class` with 
other custom validations for more advanced use cases.

```python
# example for endpoint file: api/grower.py
from acai.apigateway.requirements import requirements

from service.logic.grower import Grower
from service.logic.middlware import log_grower


# example after function
# def filter_grower(request, response, requirements):
#     if 'GET' in response.raw['message']:
#       print(response.raw)
    
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
# def log_grower(request, response, requirements):
#     print(request.body['grower_id'])
    
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
    required_path='grower/{grower_id}'
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
```
