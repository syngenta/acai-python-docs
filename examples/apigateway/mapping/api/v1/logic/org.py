import uuid

from api.v1.model.org import OrgModel


class Org:

    def __init__(self, **kwargs):
        self.__id = kwargs.get('id', str(uuid.uuid4()))
        self.__name = kwargs.get('name')
        self.__address = kwargs.get('address')
        self.__city = kwargs.get('city')
        self.__state = kwargs.get('state')

    @classmethod
    def get_by_id(cls, org_id):
        data = OrgModel.create_random(org_id=org_id)
        return cls(**data)
    
    @property
    def id(self):
        return self.__id
    
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
    
    def export(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state
        }