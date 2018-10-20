from domain.serializable import Serializable


class Product(Serializable):

    def __init__(self, account, product_name, product_id, photo_origin):
        self.account_id = account
        self.product_name = product_name
        self.product_id = product_id
        self.photo_origin = photo_origin

    def serialize(self):
        return {
            'account': self.account_id,
            'product_name': self.product_name,
            'product_id': self.product_id,
            'photo_origin': self.photo_origin
        }

    def deserialize(self, data):
        return Product(
            account=None,
            product_name=data['product_name'],
            product_id=data['product_id'],
            photo_origin=data['photo_origin']
        )

    def set_account(self, account):
        self.account_id = account
