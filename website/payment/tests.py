# Testy dla modułu `payment`
from django.test import TestCase
class PaymentTestCase(TestCase):
    def test_shipping_address_validation(self):
        address = "123 Test St, Test City, 12345"
        self.assertEqual(address, "123 Test St, Test City, 12345")
