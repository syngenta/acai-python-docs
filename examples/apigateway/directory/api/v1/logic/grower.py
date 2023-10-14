import uuid

from api.v1.model.grower import GrowerModel


class Grower:

    def __init__(self, **kwargs):
        self.__id = kwargs.get('id', str(uuid.uuid4()))
        self.__email = kwargs.get('email')
        self.__phone = kwargs.get('phone')
        self.__first = kwargs.get('first')
        self.__last = kwargs.get('last')
    
    @classmethod
    def get_all(cls, **kwargs):
        grower_model = GrowerModel() 
        grower_data = grower_model.get_all(kwargs.get('limit', 10), kwargs.get('first'), kwargs.get('last'))
        return [cls(**data) for data in grower_data]
    
    @classmethod
    def get_by_id(cls, **kwargs):
        grower_data = GrowerModel.create_random(grower_id=kwargs['grower_id'])
        return cls(**grower_data)
    
    @property
    def id(self):
        return self.__id
    
    @property
    def email(self):
        return self.__email

    @property
    def phone(self):
        return self.__phone

    @property
    def first(self):
        return self.__first

    @property
    def last(self):
        return self.__last
    
    def update(self, **kwargs):
        for grower_key in kwargs:
            setattr(self, f'_Grower__{grower_key}', kwargs[grower_key])

    def export(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'first': self.first,
            'last': self.last
        }