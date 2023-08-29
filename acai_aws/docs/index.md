# Acai AWS
DRY, configurable, declarative node library for working with Amazon Web Service Lambdas.

## Features
* Highly configurable apigateway internal router
* Openapi schema adherence for all event types
* Extensible and customizable middleware for validation and other tasks
* DRY coding interfaces without the need of boilerplate
* Ease-of-use with the [serverless framework](https://www.serverless.com/)
* Local Development support
* Happy Path Programming (See Philosophy below)

## Philosophy

The Acai philosophy is to provide a dry, configurable, declarative library for use with the amazon lambdas, which encourages Happy Path Programming (HPP).

Happy Path Programming is an idea in which inputs are all validated before operated on. This ensures code follows the happy path without the need for mid-level, nested exceptions and all the nasty exception handling that comes with that. The library uses layers of customizable middleware options to allow a developer to easily dictate what constitutes a valid input, without nested conditionals, try/catch blocks or other coding blocks which distract from the happy path that covers the majority of that codes intended operation.
