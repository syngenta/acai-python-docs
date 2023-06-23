---
title: Request
description: Acai Request Object
---

# Request Object

By default, every endpoint function will receive an instance of the `Request` class (aka `request`) as the first argument of their function. This `request` has a lot of properties which will do common things automatically, but still allows the developer to override those operations if they deem necessary. Below is a list and examples of all the properties of the `request`:

???+ example
    Don't like reading documentation? Then look at [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/apigateway) which can run locally! :nerd:

### Request Properties

| property                                                              |  type  | mutable | description                                                   |
|:----------------------------------------------------------------------|:------:|:-------:|:--------------------------------------------------------------|
| [`method`]({{web.url}}/apigateway/request/#requestmethod)             |  str   |   no    | the http method of the request                                |
| [`cookies`]({{web.url}}/apigateway/request/#requestcookies)           |  list  |   no    | the cookies of the request                                    |
| [`protocol`]({{web.url}}/apigateway/request/#requestprotocol)         |  str   |   no    | the protocol of the request                                   |
| [`content_type`]({{web.url}}/apigateway/request/#requestcontent_type) |  str   |   no    | the content_type of the request body                          |
| [`host_url`]({{web.url}}/apigateway/request/#requesthost_url)         |  str   |   no    | the host_url of the request was sent to                       |
| [`domain`]({{web.url}}/apigateway/request/#requestdomain)             |  str   |   no    | the domain of the request was sent to                         |
| [`stage`]({{web.url}}/apigateway/request/#requeststage)               |  str   |   no    | the stage the lambda was deployed to                          |
| [`resource`]({{web.url}}/apigateway/request/#requestresource)         |  str   |   no    | the AWS resource being invoked                                |
| [`authorizer`]({{web.url}}/apigateway/request/#requestauthorizer)     | object |   no    | if using a customized authorizer, the authorizer object       |
| [`headers`]({{web.url}}/apigateway/request/#requestheaders)           | object |   no    | the headers of the request                                    |
| [`params`]({{web.url}}/apigateway/request/#requestparams)             | object |   no    | combination of query string and path params in one object     |
| [`query_params`]({{web.url}}/apigateway/request/#requestquery_params) | object |   no    | query string parameters from the request                      |
| [`path_params`]({{web.url}}/apigateway/request/#requestpath_params)   | object |   no    | the path parameters of the request                            |
| [`route`]({{web.url}}/apigateway/request/#requestroute)               |  str   |   no    | the requested route with placeholders of params               |
| [`path`]({{web.url}}/apigateway/request/#requestpath)                 |  str   |   no    | the raw requested path with actual param values               |
| [`json`]({{web.url}}/apigateway/request/#requestjson)                 | object |   no    | the body of the request, converted from json string in object |
| [`xml`]({{web.url}}/apigateway/request/#requestxml)                   | object |   no    | the body of the request, converted from xml string in object  |
| [`graphql`]({{web.url}}/apigateway/request/#requestgraphql)           |  str   |   no    | the body of the graphql request as a string                   |
| [`body`]({{web.url}}/apigateway/request/#requestbody)                 |  any   |   no    | the body of the request, converted to based on data type      |
| [`raw`]({{web.url}}/apigateway/request/#requestraw)                   |  any   |   no    | the raw body of the request no conversion                     |
| [`context`]({{web.url}}/apigateway/request/#requestcontext)           | object |   yes   | mutable request context to assigned and pass around           |
| [`event`]({{web.url}}/apigateway/request/#requestevent)               | object |   no    | the full event originally coming from the lambda              |

#### `request.cookies`

```python
print(request.cookies)

# output: 
['some-cookie']
```

#### `request.protocol`

```python
print(request.cookies)

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
    apiKey: 'SOME KEY',
    userId: 'x-1-3-4',
    correlationId: 'abc12312',
    principalId: '9de3f415a97e410386dbef146e88744e',
    integrationLatency: 572
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
    query: {
        name: 'me'
    },
    path: {
        id: 1
    }
}
```

#### `request.query_params`

```python
print(request.query_params)

# output:
{
     name: 'me'
}
```

#### `request.path_params`

```python

print(request.path_params)

# output:
{
     id: 1
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
    some_json_key: 'some_json_value'
}
```

```python

print(request.form);

# output:
{
    some_form_key: 'some_form_value'
}
```

#### `request.xml`

???+ warning
    This will raise an unhandled exception if the body is not xml compatible

```python
python(request.xml);

# output:
{
    some_xml_key: 'some_xml_value'
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
    some_key: 'some_value'
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
    application_assignable: true
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
    "isBase64Encoded": false,
    "stageVariables": {
        "stageVariable1": "value1",
        "stageVariable2": "value2"
    }
}
```
