# coding=utf-8

import json
import unittest
from geopy.geocoders import Nominatim
from domain.product import Product
from domain.searchedproduct import SearchedProduct
from services import distancesort


class BaseTest(unittest.TestCase):
    def test_json(self):
        j = '{"fruits": ["apple", "banana", "orange"]}'
        data = json.loads(j)
        self.assertEqual(data['fruits'][0], 'apple')
        j1 = '{"fruits": {"1":"apple", "2":"banana", "3":"orange"}}'
        dat2 = json.loads(j1)
        self.assertEqual(dat2['fruits']['1'], 'apple')
        j2 = '{"category_name": "Холодные напитки",' \
             '"photo_origin": "/upload/pos_cdb_67169/menu/product_1540043162_6.jpg",' \
             '"price": {"1": "7500"},' \
             '"product_id": "6",' \
             '"product_name": "Лимонад",' \
             '"spots": [{"spot_id": "1","price": "7500","profit": "6500","visible": "1"}]' \
             '}'
        p = Product.deserialize(json.loads(j2))
        self.assertEqual(p.product_name, u'Лимонад')
        self.assertEqual(p.price, '7500')

    def test_geo(self):
        geolocator = Nominatim(user_agent="foodle")
        location = geolocator.geocode("175 5th Avenue NYC")
        self.assertTrue(location.address.index('New York'))

    def test_sortnig(self):
        arr=[SearchedProduct(1,100),
        SearchedProduct(2, 100),
        SearchedProduct(4, 100),
        SearchedProduct(5, 100),
        SearchedProduct(6, 100),
        SearchedProduct(3, 100),
        SearchedProduct(7, 100),
        SearchedProduct(9, 100),
        SearchedProduct(8, 100),
        SearchedProduct(10, 100)]

        base = SearchedProduct(11,100)

        new_arr = distancesort.sort_by_distance(arr, base.lat, base.long)

        self.assertEquals(new_arr[0], arr[9])
