from acai_aws.apigateway.requirements import requirements

from api.v1.shared.validator import Validator
from api.v1.org.org_logic import Org


@requirements(required_headers=['x-org-id'], before=Validator.org_exists)
def get(request, response):
    org = Org.get_by_id(request.headers['x-org-id'])
    response.body = org.export()
    return response


@requirements(required_body='post-org-request')
def post(request, response):
    org = Org(**request.body)
    response.body = org.export()
    return response