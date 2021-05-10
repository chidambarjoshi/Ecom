from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from com.models import Users,Category,Product,product_image


# Create your tests here.
class TestViews(APITestCase):
    def test_search_category_POST(self):
        user = Users.objects.get(email='chidambar.joshi5@gmail.com')
        client = APIClient()
        client.force_authenticate(user=user)
        data={"search":"el"}
        response=client.post('http://127.0.0.1:8000/api/category/search/',data)
        print(response.status_code)
        self.assertEqual(response.status_code,200)