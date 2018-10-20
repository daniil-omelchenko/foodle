from domain.serializable import Serializable


class Product(Serializable):

    def __init__(self, product_name, product_id, photo_origin):
        self.product_name = product_name
        self.product_id = product_id
        self.photo_origin = photo_origin

    def serialize(self):
        return {
            'product_name': self.product_name,
            'product_id': self.product_id,
            'photo_origin': self.photo_origin
        }

    def deserialize(self, data):
        return Product(
            product_name=data['product_name'],
            product_id=data['product_id'],
            photo_origin=data['photo_origin']
        )
