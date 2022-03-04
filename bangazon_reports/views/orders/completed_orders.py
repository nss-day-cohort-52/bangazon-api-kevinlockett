"""Module for generating Expensive Products Report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class CompletedOrders(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            #Execute SQLite3 query:
            db_cursor.execute("""    
            SELECT
                bangazon_api_order.id AS order_id,
                (auth_user.first_name || " " || auth_user.last_name) AS customer_name,
                sum(bangazon_api_product.price) AS total_paid,
                bangazon_api_paymenttype.merchant_name AS payment_type
            FROM bangazon_api_order
            JOIN auth_user
                ON bangazon_api_order.user_id = auth_user.id
            JOIN bangazon_api_paymenttype
                ON bangazon_api_order.payment_type_id = bangazon_api_paymenttype.id
            JOIN bangazon_api_orderproduct
                ON bangazon_api_order.id = bangazon_api_orderproduct.order_id
            JOIN bangazon_api_product
                ON bangazon_api_orderproduct.product_id = bangazon_api_product.id
            WHERE payment_type_id NOT NULL
            GROUP BY order_id;
            """)
            
            #Pass the the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            #Convert flat data from dataset into a json-like datastructure
            orders = []
            for row in dataset:
                
                #Create a dictionary that includes all required SQL columns
                order = {
                    'order_id': row['order_id'],
                    'customer_name': row['customer_name'],
                    'total_paid': row['total_paid'],
                    'payment_type': row['payment_type']
                }
                #The append needs to be within the scope of the products dictionary or it will only load the last item in the list                
                orders.append(order)
            # The template string must match the file name of the html template
            template = 'completed_orders.html'
        
            # The context will be a dictionary that the template can access to show data
            context = {
                "completed_orders_list": orders
            }

            return render(request, template, context)