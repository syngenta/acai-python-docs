import uuid

from api.v1.farm._farm_id.field.field_model import FieldModel


class Field:

    def __init__(self, **kwargs):
        self.__farm_id = kwargs['farm_id']
        self.__id = kwargs.get('id', str(uuid.uuid4()))
        self.__name = kwargs.get('name')
        self.__coordinates = kwargs.get('coordinates')

    @classmethod
    def get_all(cls, **kwargs):
        field_model = FieldModel() 
        field_data = field_model.get_all(kwargs['farm_id'], kwargs.get('limit', 10), kwargs.get('name'))
        return [cls(**data) for data in field_data]
    
    @classmethod
    def get_by_id(cls, **kwargs):
        field_data = FieldModel.create_random(field_id=kwargs['field_id'], farm_id=kwargs['farm_id'])
        return cls(**field_data)

    @property
    def id(self):
        return self.__id

    @property
    def farm_id(self):
        return self.__farm_id

    @property
    def name(self):
        return self.__name

    @property
    def coordinates(self):
        return self.__coordinates
    
    def update(self, **kwargs):
        for field_key in kwargs:
            setattr(self, f'_Field__{field_key}', kwargs[field_key])

    def export(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'name': self.name,
            'coordinates': self.coordinates
        }