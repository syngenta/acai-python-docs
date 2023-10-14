handler_routes = {
    'org': 'api/v1/handler/org.py',
    'grower': 'api/v1/handler/grower/__init__.py',
    'grower/{grower_id}': 'api/v1/handler/grower/grower_id.py',
    'farm': 'api/v1/handler/farm/__init__.py',
    'farm/{farm_id}': 'api/v1/handler/farm/farm_id.py',
    'farm/{farm_id}/field': 'api/v1/handler/field/__init__.py',
    'farm/{farm_id}/field/{field_id}': 'api/v1/handler/field/field_id.py'
}