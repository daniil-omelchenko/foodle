from models import ProductModel, SpotModel, SpotProductModel, AccountModel


class SearchedProduct:
    def __init__(self, product, spot, account, spotproduct):
        # type: (ProductModel, SpotModel, AccountModel, SpotProductModel) -> None
        self.product_name = product.product_name
        self.price = spotproduct.price
        self.currency = account.currency
        self.spot_name = spot.spot_name
        self.image = product.photo_url
        self.address = spot.spot_adress
        self.long = spot.long
        self.lat = spot.lat
