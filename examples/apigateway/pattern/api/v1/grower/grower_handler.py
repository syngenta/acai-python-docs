from acai_aws.apigateway.requirements import requirements

from api.v1.grower.grower_logic import Grower


@requirements(available_query=['first', 'last', 'limit'])
def get(request, response):
    growers = Grower.get_all(
        first=request.query_params.get('first'), 
        last=request.query_params.get('last'), 
        limit=request.query_params.get('limit', 10)
    )
    response.body = {'growers': [grower.export() for grower in growers]}
    return response


@requirements(required_body='post-grower-request')
def post(request, response):
    grower = Grower(**request.body)
    response.body = grower.export()
    return response