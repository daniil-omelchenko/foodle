from domain.serializable import Serializable


class Product(Serializable):

    def __init__(self, product_name, product_id, photo_origin):
        # type: (str, str, str) -> None
        self.product_name = product_name
        self.product_id = product_id
        self.photo_origin = photo_origin

    def serialize(self):
        # type: () -> dict
        return {
            'product_name': self.product_name,
            'product_id': self.product_id,
            'photo_origin': self.photo_origin
        }

    @classmethod
    def deserialize(cls, data):
        # type: (dict) -> Product
        return Product(
            product_name=data['product_name'],
            product_id=data['product_id'],
            photo_origin=data['photo_origin']
        )
