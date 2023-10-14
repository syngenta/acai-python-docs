from acai_aws.apigateway.requirements import requirements

from api.v1.farm._farm_id.field.field_logic import Field


@requirements(required_route='/v1/farm/{farm_id}/field/{field_id}')
def get(request, response):
    field = Field.get_by_id(
        farm_id=request.path_params['farm_id'],
        field_id=request.path_params['field_id']
    )
    response.body = field.export()
    return response


@requirements(required_route='/v1/farm/{farm_id}/field/{field_id}')
def patch(request, response):
    field = Field.get_by_id(
        farm_id=request.path_params['farm_id'],
        field_id=request.path_params['field_id']
    )
    field.update(**request.body)
    response.body = field.export()
    return response


@requirements(required_route='/v1/farm/{farm_id}/field/{field_id}')
def delete(request, response):
    field_id = request.path_params['field_id']
    response.body = {'message': f'field {field_id} has been deleted'}
    return response