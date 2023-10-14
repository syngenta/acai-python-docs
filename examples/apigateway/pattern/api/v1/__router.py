from acai_aws.apigateway.router import Router


router = Router(
    base_path='pattern-example/v1',
    handlers='api/v1/**/*_handler.py',
    schema='api/openapi.yml'
)
router.auto_load()

def route(event, context):
    return router.route(event, context)