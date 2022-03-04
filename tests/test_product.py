import random
import faker_commerce
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.helpers import STATE_NAMES
from bangazon_api.models import Category, OrderProduct, Product


class ProductTests(APITestCase):
    def setUp(self):
        """
        Create auth users & user token
        """
        call_command('seed_db', user_count=2)
        self.user1 = User.objects.filter(store__isnull=False).first()
        self.token = Token.objects.get(user=self.user1)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        category = Category.objects.first()

        data = {
            "name": self.faker.ecommerce_name(),
            "price": random.randint(50, 1000),
            "description": self.faker.paragraph(),
            "quantity": random.randint(2, 20),
            "location": random.choice(STATE_NAMES),
            "imagePath": "",
            "categoryId": category.id
        }
        response = self.client.post('/api/products', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])

    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        product = Product.objects.first()
        data = {
            "name": product.name,
            "price": product.price,
            "description": self.faker.paragraph(),
            "quantity": product.quantity,
            "location": product.location,
            "imagePath": "",
            "categoryId": product.category.id
        }
        response = self.client.put(f'/api/products/{product.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        product_updated = Product.objects.get(pk=product.id)
        self.assertEqual(product_updated.description, data['description'])

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())
        
    def test_delete_product(self):
        """
        Ensure we can delete a product
        """        
        # Define a product to delete - use the first product in the table.
        product = Product.objects.first()
        response = self.client.delete(f'/api/products/{product.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_product_to_current_order(self):
        """
        Ensure items added to cart are placed on open order
        """
        
        #Add an item to an order
        product = Product.objects.first()
        product_response = self.client.post(f'/api/products/{product.id}/add_to_order')
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)
        
        #Get current user's current order
        order_response = self.client.get('/api/orders/current')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        
        #Ensure product is in current order
        self.assertIsNotNone(OrderProduct.objects.get(
            order=order_response.data["id"], product=product
        ))
    
    def test_rate_product(self):
        """
        Ensure we can add a rating to a product and average rating is updated and correct
        """
        #Create product to rate - select first product from table
        product = Product.objects.first()
        
        #Create rating dictionary for product
        rating = {
            "score": random.randint(1, 5),
            "review": self.faker.paragraph()
        }
        
        #Post product rating & get product
        response = self.client.post(f'/api/products/{product.id}/rate-product', rating, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f'/api/products/{product.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Calculate average of all ratings
        ratings_total = 0
        for rating in response.data['ratings']:
            ratings_total += rating['score']
            rating_average = ratings_total / len(response.data['ratings'])
        
        #Compare calculated average with data avarage
        self.assertEqual(response.data['average_rating'], rating_average)
        
        
        
        
        
        
        