import datetime
from http import HTTPStatus as status

from django.conf import settings
from django.test import TestCase
from ninja.testing import TestClient

from api.v1.product.views import router
from apps.product.log.models import ProductLog
from apps.product.models import Product


class ProductTest(TestCase):
    def setUp(self) -> None:
        self.test_product = {
            "name": "name",
            "category": "ctg",
            "manufacturer": "mnf",
            "quantity": 10,
            "unit": "string",
            "nutritional_value": 0,
            "total_net_weight": 0,
            "total_gross_weight": 0,
            "manufacture_date": "2025-01-11",
            "expiration_date": "2025-01-11",
            "notes": "string",
            "allergens": "string",
        }
        self.client = TestClient(
            router,
            headers={
                "Authorization": f"Bearer {settings.FRIDGE_PANEL_PASSWORD}",
            },
        )

    def test_product_creation(self):
        response = self.client.post("/", json=self.test_product)
        self.assertEqual(response.status_code, status.CREATED)

    def test_delete_product(self):
        product = Product(**self.test_product)
        product.full_clean()
        product.save()

        response = self.client.delete("/" + str(product.id))
        self.assertEqual(response.status_code, status.NO_CONTENT)
        self.assertRaises(
            Product.DoesNotExist, lambda: Product.objects.get(id=product.id)
        )

        response = self.client.delete("/" + str(product.id))
        self.assertEqual(response.status_code, status.NOT_FOUND)

    def test_update_product(self):
        product = Product(**self.test_product)
        product.full_clean()
        product.save()

        test_product = self.test_product.copy()
        test_product["quantity"] = 20.000
        test_product["id"] = str(product.id)

        response = self.client.put("/" + str(product.id), json=test_product)
        self.assertEqual(response.status_code, status.OK)
        for attr in test_product:
            test_product[attr] = str(test_product[attr])
        self.assertEqual(response.json(), test_product)
        self.assertEqual(
            float(Product.objects.get(id=product.id).quantity),
            float(test_product["quantity"]),
        )

    def test_get_product(self):
        response = self.client.post("/", json=self.test_product)
        id = response.json()["id"]
        expected_product = response.json()
        for attr in expected_product:
            try:
                expected_product[attr] = float(expected_product[attr])
            except ValueError:
                1 == 1

        response = self.client.get("/" + str(id))
        result_product = response.json()
        for attr in result_product:
            try:
                result_product[attr] = float(result_product[attr])
            except ValueError:
                1 == 1

        self.assertEqual(response.status_code, status.OK)
        self.assertEqual(result_product, expected_product)

        response = self.client.delete("/" + str(id))
        self.assertEqual(response.status_code, status.NO_CONTENT)
        response = self.client.get("/" + str(id))
        self.assertEqual(response.status_code, status.NOT_FOUND)

    def test_list_products(self):
        response = self.client.post("/", json=self.test_product)
        expected_product_1 = response.json()
        for attr in expected_product_1:
            try:
                expected_product_1[attr] = float(expected_product_1[attr])
            except ValueError:
                1 == 1
        response = self.client.post("/", json=self.test_product)
        expected_product_2 = response.json()
        for attr in expected_product_2:
            try:
                expected_product_2[attr] = float(expected_product_2[attr])
            except ValueError:
                1 == 1

        response = self.client.get("/")
        self.assertEqual(response.status_code, status.OK)
        result = response.json()
        for pr in result:
            for attr in pr:
                try:
                    pr[attr] = float(pr[attr])
                except ValueError:
                    1 == 1
        self.assertEqual(result, [expected_product_2, expected_product_1])

    def test_search_product(self):
        response = self.client.post("/", json=self.test_product)
        expected_product_1 = response.json()
        for attr in expected_product_1:
            try:
                expected_product_1[attr] = float(expected_product_1[attr])
            except ValueError:
                1 == 1
        response = self.client.post("/", json=self.test_product)
        expected_product_2 = response.json()
        for attr in expected_product_2:
            try:
                expected_product_2[attr] = float(expected_product_2[attr])
            except ValueError:
                1 == 1

        response = self.client.post("/search_by_qr", json=self.test_product)
        self.assertEqual(response.status_code, status.OK)
        result = response.json()
        for pr in result:
            for attr in pr:
                try:
                    pr[attr] = float(pr[attr])
                except ValueError:
                    1 == 1
        self.assertEqual(result, [expected_product_1, expected_product_2])

        no_such_product = self.test_product
        no_such_product["name"] = "no_such_name"
        response = self.client.post("/search_by_qr", json=no_such_product)
        self.assertEqual(response.json(), [])
