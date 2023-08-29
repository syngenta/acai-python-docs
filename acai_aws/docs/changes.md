---
title: 2.0 Breaking Changes
description: The changes to Acai in version 2.0
---

## Changes to the Acai AWS from 1.x to 2.0

In version 2.0 we have added a lot of cool new features, but that does require deprecating some old things. Below is a list of all the changes:

???+ tip
    If you don't want to make the changes yourself manually, we have a script which will make the changes for you. Just run this command in your terminal from the root of the directory of the project you want to upgrade:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/syngenta/acai-python-docs/main/scripts/python-upgrade.sh)"
    ```

### APIGateway

| old               | new                        | description                                                     |
|-------------------|----------------------------|-----------------------------------------------------------------|
| `router.route()`  | **`router.route(event)`**  | `router.route` now requires the event to be passed in           |
| `required_params` | **`required_query`**       | `required_query` is how you define required query string params |
| `request.params`  | **`request.query_params`** | `request.query_params` is how you access query string params    |


### DynamoDB Record

| old                        | new                     |
|----------------------------|-------------------------|
| `record.event_id`          | **`record.id`**         |
| `record.event_name`        | **`record.name`**       |
| `record.event_source`      | **`record.source`**     |
| `record.event_source_arn`  | **`record.source_arn`** |

### S3 Record

| old                        | new                     |
|----------------------------|-------------------------|
| `record.event_id`          | **`record.id`**         |
| `record.event_name`        | **`record.name`**       |
| `record.event_source`      | **`record.source`**     |
| `record.event_source_arn`  | **`record.source_arn`** |
| `record.requestParameters` | **`record.request`**    |
| `record.responseElements`  | **`record.response`**   |
| `record.s3SchemaVersion`   | **`record.version`**    |

### SNS/SQS Record

| old                       | new                     |
|---------------------------|-------------------------|
| `record.event_name`       | **`record.name`**       |
| `record.event_source`     | **`record.source`**     |
| `record.event_source_arn` | **`record.source_arn`** |
