import json
import unittest

class BaseTest(unittest.TestCase):
    def test_json(self):
        j = '{"fruits": ["apple", "banana", "orange"]}'
        data = json.loads(j)
        self.assertEqual(data['fruits'][0], 'apple')
