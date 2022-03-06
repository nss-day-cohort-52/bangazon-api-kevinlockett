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
                o.id AS order_id,
                (u.first_name || " " || u.last_name) AS customer_name,
                sum(p.price) AS total_paid,
                pt.merchant_name AS payment_type
            FROM bangazon_api_order o
            JOIN auth_user u
                ON o.user_id = u.id
            JOIN bangazon_api_paymenttype pt
                ON o.payment_type_id = pt.id
            JOIN bangazon_api_orderproduct op
                ON o.id = op.order_id
            JOIN bangazon_api_product p
                ON op.product_id = p.id
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