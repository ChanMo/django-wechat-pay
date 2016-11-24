from django.test import TestCase
from .api import Pay as PayApi

class Pay(TestCase):
    def setUp(self):
        pay = PayApi()
        data = {
            'xml': {
                'title': 'test',
            }
        }
        pay.set_prepay_id(data)

    def test_set_prepay_id(self):
        print(pay.prepay_id)

    def test_get_pay_data():
        print(pay.get_pay_data())
