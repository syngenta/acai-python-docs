from acai_aws.apigateway.requirements import requirements

from api.v1.logic.farm import Farm


@requirements(
    required_query=['org_id'],
    available_query=['name', 'limit']
)
def get(request, response):
    farms = Farm.get_all(
        org_id=request.query_params['org_id'], 
        limit=request.query_params.get('limit', 10)
    )
    response.body = {'farms': [farm.export() for farm in farms]}
    return response


@requirements(required_body='post-farm-request')
def post(request, response):
    farm = Farm(**request.body)
    response.body = farm.export()
    return response