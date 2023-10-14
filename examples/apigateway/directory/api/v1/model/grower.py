from chance import chance

# let's pretend this is a database model
class GrowerModel:

    def get_grower_by_id(self, grower_id):
        if grower_id.startswith('acai'):
            return GrowerModel.create_random(grower_id=grower_id)
        return None
    
    def create(self, grower):
        pass

    def update(self, grower_id, grower):
        pass

    def delete(self, grower_id, grower):
        pass

    def get_all(self, limit=10, filter_first=None, filter_last=None):
        growers = []
        for i in range(int(limit)):
            add_grower = True
            if filter_first is not None or filter_last is not None:
                add_grower = chance.boolean(likelihood=10)
            grower = GrowerModel.create_random()
            grower['first'] = filter_first if filter_first else grower['first']
            grower['last'] = filter_last if filter_last else grower['last']
            if add_grower:
                growers.append(grower)
        return growers

    @staticmethod  
    def create_random(**kwargs):
        return {
            'id': kwargs.get('grower_id', chance.hex_hash()),
            'email': chance.email(),
            'phone': chance.phone(),
            'first': chance.first(),
            'last': chance.last()
        }