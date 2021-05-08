from rest_framework.test import APITestCase,APIClient
from django.urls import reverse


# Create your tests here.
class TestViews(APITestCase):
    def test_search_category_GET(self):
        client=APIClient()
        data={"search":"el"}
        response=client.get('http://127.0.0.1:8000/api/category/search/',data,format='json')
        print(response.status_code)
        self.assertEqual(response.status_code,200)