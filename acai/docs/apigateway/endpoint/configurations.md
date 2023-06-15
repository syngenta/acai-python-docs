---
title: Configurations
description: How to use the built-in validation & custom middleware
---

# Endpoint Configurations

In order to encourage "Happy Path Programming" and make it easier for developers to validate request fully, the Acai comes with a host of built-in validations as well as the ability to extend with custom validations and middleware. See the full validation list here:

???+ examples
    Don't like reading documentation? Then look at [our examples,](https://github.com/syngenta/acai-python-docs/blob/main/examples/apigateway) which can run locally! :nerd:

### Validation Configurations

| requirement                                                                                | type  | description                                                   |
|--------------------------------------------------------------------------------------------|-------|---------------------------------------------------------------|
| **[`requiredHeaders`]({{web.url}}/apigateway/endpoint/configurations/#requiredheaders)**   | array | every header in this array must be in the headers of request  |
| **[`availableHeaders`]({{web.url}}/apigateway/endpoint/configurations/#availableheaders)** | array | only headers in this array will be allowed in the request     |
| **[`requiredQuery`]({{web.url}}/apigateway/endpoint/configurations/#requiredquery)**       | array | every item in the array is a required query string parameter  |
| **[`availableQuery`]({{web.url}}/apigateway/endpoint/configurations/#availablequery)**     | array | only items in this array are allowed in the request           |
| **[`requiredPath`]({{web.url}}/apigateway/endpoint/configurations/#requiredpath)**         | str   | when using parameters, this is the required parameters        |
| **[`requiredBody`]({{web.url}}/apigateway/endpoint/configurations/#requiredbody)**         | str   | references a JSschema component in your `schemaFile`          |
| **[`requiredAuth`]({{web.url}}/apigateway/endpoint/configurations/#requiredauth)**         | bool  | will trigger `withAuth` function defined in the router config |
| **[`before`]({{web.url}}/apigateway/endpoint/configurations/#before)**                     | func  | a custom function to be ran before your method function       |
| **[`after`]({{web.url}}/apigateway/endpoint/configurations/#after)**                       | func  | a custom function to be ran after your method function        |
| **[`dataClass`]({{web.url}}/apigateway/endpoint/configurations/#dataclass)**               | class | a custom class that will be passed instead of the request obj |
| **[`custom-requirement`]**                                                                 | any   | see bottom of page                                            |

#### `requiredHeaders`

???+ info
    Headers are case-sensitive, make sure your casing matches your expectations.

```js

exports.requirements = {
    post: {
        requiredHeaders: ['x-onbehalf-of']
    }
};
```

#### `availableHeaders`

???+ warning
    This is not recommended for frequent use as it raises errors for every header which does not conform to the array provided. Many browsers, http tools, and libraries will automatically add headers to request, unbeknownst to the user. By using this setting, you will force every user of the endpoint to take extra care with the headers provided and may result in poor API consumer experience.

```js

exports.requirements = {
    post: {
        availableHeaders: ['x-onbehalf-of']
    }
};
```

#### `requiredQuery`

```js

exports.requirements = {
    get: {
        requiredQuery: ['requester_id']
    }
};
```

#### `availableQuery`

```js

exports.requirements = {
    get: {
        availableQuery: ['grower_email', 'grower_phone', 'grower_first', 'grower_last'],
    }
};
```

#### `requiredPath`

???+ warning
    This is required if you are using dynamic routing (ex. `{id}.js`) with path parameters. The router will provide a path values in `request.pathParams`

```js

exports.requirements = {
    put: {
        requiredPath: 'grower/{id}'
    }
};
```

#### `requiredBody`

???+ info
    This is referencing a `components.schemas` section of your openapi.yml file defined in the `schemaFile` value in your router config.

```js

exports.requirements = {
    post: {
        requiredBody: 'post-grower-request'
    }
};
```


#### `requiredAuth`

???+ info
    This will trigger the function you provided in the router config under the `withAuth` configuration

```js

exports.requirements = {
    post:{
        requiredAuth: true
    }
};
```

#### `before`

```js

exports.requirements = {
    patch: {
        before: async (request, response, requirements) => {
            const result = await db.checkGrowerIdExists(request.pathParams.id);
            if (!result){
                response.setError('grower/{id}', `grower with id: ${id} does not exist.`);
            }
        }
    }
};
```

#### `after`

```js

exports.requirements = {
    get: {
        after: async (request, response, requirements) => {
            const relations = await db.getRequesterRelations(request.headers['x-requester-id']);
            const results = []
            for (const grower in response.rawBody){
                if (relations.includes(grower.id)){
                    results.push(grower);
                }
            }
            response.body = results;
            return response;
        }
    }
};
```

#### `dataClass`

???+ info
    Instead of getting a `request` and `response` as arguments passed to your API function, you will get an instance of the class you provided here

```js

exports.requirements = {
    post: {
        dataClass: Grower
    }
};
```

#### custom requirements (example)

???+ info
    You can add as many custom requirements as you want, with any variable type you want, and they will be passed to your `beforeAll`, `before`, `afterAll`, `after` and `withAuth` middleware defined functions.

```js

exports.requirements = {
    post:{
        myCustomBeforeAllPermission: {permission: 'allow-delete-grower'}
    }
};
```
