from django.test import TestCase
from store.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile

class CartTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product", 
            price=10.0, 
            category=self.category,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_add_product_to_cart(self):
        cart = {}
        cart[str(self.product.id)] = {"quantity": 1, "price": self.product.price}
        self.assertIn(str(self.product.id), cart)

    def test_remove_product_from_cart(self):
        cart = {str(self.product.id): {"quantity": 1, "price": self.product.price}}
        cart.pop(str(self.product.id), None)
        self.assertNotIn(str(self.product.id), cart)

    def test_cart_summary(self):
        cart = {str(self.product.id): {"quantity": 2, "price": self.product.price}}
        total_price = sum(item["quantity"] * item["price"] for item in cart.values())
        self.assertEqual(total_price, 20.0)