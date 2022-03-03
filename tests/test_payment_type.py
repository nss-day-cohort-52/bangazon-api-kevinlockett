from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.models import PaymentType

class PaymentTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()


    def test_create_payment_type(self):
        """
        Ensure we can add a payment type for a customer.
        """
        # Add a payment type to order
        data = {
            "merchant": self.faker.credit_card_provider(),
            "acctNumber": self.faker.credit_card_number()
        }

        response = self.client.post('/api/payment-types', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data["merchant_name"], data['merchant'])
        self.assertEqual(response.data["obscured_num"][-4:], data['acctNumber'][-4:])
        
    def test_delete_payment_type(self):
        """
        Ensure we can delete a payment type for a customer
        """
        
        # Add a payment type to delete
        payment_type = PaymentType()
        payment_type.merchant_name = self.faker.credit_card_provider(),
        payment_type.acct_number = self.faker.credit_card_number(),
        payment_type.customer_id = self.user1.id
        payment_type.save()
        
        response = self.client.delete(f'/api/payment-types/{payment_type.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)