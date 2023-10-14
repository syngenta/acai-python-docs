import random
from chance import chance


# let's pretend this is a database model
class FarmModel:
    
    def get_farm_by_id(self, org_id=None, farm_id=None):
        if farm_id:
            return FarmModel.create_random(farm_id=farm_id, org_id=org_id)
        return None
    
    def create(self, farm):
        pass

    def update(self, farm_id, farm):
        pass

    def delete(self, farm_id, farm):
        pass

    def get_all(self, org_id, limit=10, name_filter=None):
        farms = []
        for i in range(int(limit)):
            add_farm = True
            if name_filter is not None:
                add_farm = chance.boolean(likelihood=10)
            farm = FarmModel.create_random(org_id=org_id)
            farm['name'] = name_filter if name_filter else farm['name']
            if add_farm:
                farms.append(farm)
        return farms

    @staticmethod  
    def create_random(**kwargs):
        return {
            'id': kwargs.get('farm_id', chance.hex_hash()),
            'org_id': kwargs.get('org_id', chance.hex_hash()),
            'name': chance.name(),
            'address': chance.street(),
            'city': chance.city(),
            'state': chance.state()
        }