import random
from chance import chance

from api.v1.model.farm import FarmModel as Farm

# let's pretend this is a database model
class OrgModel:

    def get_org_by_id(self, org_id=None):
        if org_id:
            return OrgModel.create_random(org_id=org_id)
        return None
    
    def create(self, org):
        pass

    def update(self, org_id, org):
        pass

    def delete(self, org_id, org):
        pass

    def get_farms(self, org_id):
        farms = []
        for i in range(10):
            farms.append(Farm.create_random(org_id=org_id))
        return farms
    
    @staticmethod  
    def create_random(**kwargs):
        return {
            'id': kwargs.get('org_id', chance.hex_hash()),
            'name': chance.name(),
            'address': chance.street(),
            'city': chance.city(),
            'state': chance.state()
        }