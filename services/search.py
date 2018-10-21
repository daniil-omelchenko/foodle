from domain.searchedproduct import SearchedProduct
from services import storage


def create_searched_product(product, spot, account, spotproduct):
    return SearchedProduct(product, spot, account, spotproduct)


def find_products(search_request):
    products = storage.get_products(search_request)
    search_results = []
    for product in products:
        search_results.append(create_searched_product(storage.find_related_modles(product)))
    return search_results