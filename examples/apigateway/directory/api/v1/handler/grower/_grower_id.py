from acai_aws.apigateway.requirements import requirements

from api.v1.logic.grower import Grower


@requirements(required_route='/v1/grower/{grower_id}')
def get(request, response):
    grower = Grower.get_by_id(grower_id=request.path_params['grower_id'])
    response.body = grower.export()
    return response


@requirements(
    required_route='/v1/grower/{grower_id}',
    required_body='patch-grower-request'
)
def patch(request, response):
    grower = Grower.get_by_id(grower_id=request.path_params['grower_id'])
    grower.update(**request.body)
    response.body = grower.export()
    return response


@requirements(required_route='/v1/grower/{grower_id}')
def delete(request, response):
    grower_id = request.path_params['grower_id']
    response.body = {'message': f'grower {grower_id} has been deleted'}
    return response