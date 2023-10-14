from acai_aws.apigateway.requirements import requirements

from api.v1.farm._farm_id.field.field_logic import Field


@requirements(
    required_route='/v1/farm/{farm_id}/field', 
    available_query=['name', 'limit']
)
def get(request, response):
    fields = Field.get_all(
        farm_id=request.path_params['farm_id'], 
        limit=request.query_params.get('limit', 10)
    )
    response.body = {'fields': [field.export() for field in fields]}
    return response


@requirements(
    required_route='/v1/farm/{farm_id}/field',
    required_body='post-field-request'
)
def post(request, response):
    field_data = request.body
    field_data['farm_id'] = request.path_params['farm_id']
    field = Field(**field_data)
    response.body = field.export()
    return response