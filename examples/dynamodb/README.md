# Acai AWS Python DynamoDB Example

A simple deployable example of how to use ACAI with DynamoDB Streams

## Run Locally

```bash
$ pipenv install --dev
$ npm install
$ npm run serverless -- dynamodb install
# download and install java (if you haven't) https://www.java.com
$ npm start
# this must continue running, but in a separate terminal window run the following:
$ npm run ddb
```