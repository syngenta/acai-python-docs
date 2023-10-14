from chance import chance

# let's pretend this is a database model
class FieldModel:
    
    def get_field_by_id(self, field_id, farm_id):
        if field_id.startswith('acai'):
            return FieldModel.create_random(field_id=field_id, farm_id=farm_id)
        return None
    
    def create(self, field):
        pass

    def update(self, field_id, field):
        pass

    def delete(self, field_id, field):
        pass

    def get_all(self, farm_id, limit=10, name_filter=None):
        fields = []
        for i in range(int(limit)):
            add_field = True
            if name_filter is not None:
                add_field = chance.boolean(likelihood=10)
            field = FieldModel.create_random(farm_id=farm_id)
            field['name'] = name_filter if name_filter else field['name']
            if add_field:
                fields.append(field)
        return fields

    @staticmethod  
    def create_random(**kwargs):
        return {
            'id': kwargs.get('field_id', chance.hex_hash()),
            'farm_id': kwargs.get('farm_id'),
            'name': chance.name(),
            'coordinates': [chance.ip(), chance.ip()]
        }