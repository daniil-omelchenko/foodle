from domain.serializable import Serializable


class Product(Serializable):

    def __init__(self, product_name, product_id, photo_url, category_name, spots):
        # type: (str, str, str, float, str) -> None
        self.product_name = product_name
        self.product_id = product_id
        self.photo_url = photo_url
        self.category_name = category_name
        self.spots= spots

    def serialize(self):
        # type: () -> dict
        return {
            'product_name': self.product_name,
            'product_id': self.product_id,
            'photo_url': self.photo_url
        }

    @classmethod
    def deserialize(cls, data):
        # type: (dict) -> Product
        return Product(
            product_name=data['product_name'],
            product_id=data['product_id'],
            photo_url='https://joinposter.com{}'.format(data['photo_origin']),
            category_name=data['category_name'],
            spots=data['spots']
        )
