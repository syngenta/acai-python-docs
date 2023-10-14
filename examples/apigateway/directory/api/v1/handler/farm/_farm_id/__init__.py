from acai_aws.apigateway.requirements import requirements

from api.v1.logic.farm import Farm


@requirements(required_route='/v1/farm/{farm_id}')
def get(request, response):
    farm = Farm.get_by_id(farm_id=request.path_params['farm_id'])
    response.body = farm.export()
    return response


@requirements(
    required_route='/v1/farm/{farm_id}',
    required_body='patch-farm-request'
)
def patch(request, response):
    farm = Farm.get_by_id(farm_id=request.path_params['farm_id']) 
    farm.update(**request.body)
    response.body = farm.export()
    return response


@requirements(required_route='/v1/farm/{farm_id}')
def delete(request, response):
    farm_id = request.path_params['farm_id']
    response.body = {'message': f'farm {farm_id} has been deleted'}
    return response