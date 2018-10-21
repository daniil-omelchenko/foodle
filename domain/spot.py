from domain.serializable import Serializable


class Spot(Serializable):

    def __init__(self, spot_id, spot_name, spot_address):
        # type: (str, str, str) -> None
        self.spot_id = spot_id
        self.spot_name = spot_name
        self.spot_address = spot_address

    def serialize(self):
        # type: () -> dict
        return {
            'spot_id': self.spot_id,
            'spot_name': self.spot_name,
            'spot_address': self.spot_address
        }

    @classmethod
    def deserialize(cls, data):
        # type: (dict) -> Spot
        return Spot(
            spot_id=data['spot_id'],
            spot_name=data['spot_name'],
            spot_address=data.get('spot_adress') or data.get('spot_address')
        )
