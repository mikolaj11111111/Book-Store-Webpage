from django.test import TestCase
from store.models import Product, Category
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class StoreTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product", 
            price=10.0, 
            category=self.category,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_product_page_view(self):
        response = self.client.get(f"/product/{self.product.id}/")
        self.assertEqual(response.status_code, 200)

    def test_product_search(self):
        response = self.client.get("/search/?query=Test")
        self.assertEqual(response.status_code, 200)

    def test_product_model_str(self):
        self.assertEqual(str(self.product), "Test Product")