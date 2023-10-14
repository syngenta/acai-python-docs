class Validator:
    
    def grower_is_unique(request, response, requirements):
        if True == False:
            response.set_error('some_id', 'grower is not unique; already found grower with that information')
            return False
        return True

    def grower_exists(request, response, requirements):
        if True == False:
            response.set_error('some_id', 'grower does not exist in our system')
            return False
        return True

    def org_exists(request, response, requirements):
        if True == False:
            response.set_error('some_id', 'org does not exist in our system')
            return False
        return True

    def farm_exists(request, response, requirements):
        if True == False:
            response.set_error('some_id', 'farm does not exist in our system')
            return False
        return True