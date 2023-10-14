from api.v1.farm.farm_model import FarmModel


class Farm:

    def __init__(self, **kwargs):
        self.__org_id = kwargs['org_id']
        self.__id = kwargs.get('id')
        self.__name = kwargs.get('name')
        self.__address = kwargs.get('address')
        self.__city = kwargs.get('city')
        self.__state = kwargs.get('state')
    
    @classmethod
    def get_all(cls, **kwargs):
        farm_model = FarmModel() 
        farm_data = farm_model.get_all(kwargs['org_id'], kwargs.get('limit', 10), kwargs.get('name'))
        return [cls(**data) for data in farm_data]

    @classmethod
    def get_by_id(cls, **kwargs):
        farm_data = FarmModel.create_random(farm_id=kwargs['farm_id'])
        return cls(**farm_data)

    @property
    def id(self):
        return self.__id
    
    @property
    def org_id(self):
        return self.__org_id
    
    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address

    @property
    def city(self):
        return self.__city

    @property
    def state(self):
        return self.__state

    def update(self, **kwargs):
        for farm_key in kwargs:
            setattr(self, f'_Farm__{farm_key}', kwargs[farm_key])
    
    def export(self):
        return {
            'org_id': self.org_id,
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state
        }