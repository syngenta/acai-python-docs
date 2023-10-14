from acai_aws.apigateway.router import Router

from api.v1.routes import handler_routes


router = Router(
    base_path='mapping-example/v1',
    handlers=handler_routes,
    schema='api/openapi.yml'
)
router.auto_load()


def route(event, context):
    return router.route(event, context)