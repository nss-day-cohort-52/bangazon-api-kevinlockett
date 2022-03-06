"""Module for generating Expensive Products Report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class InexpensiveProducts(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            #Execute SQLite3 query:
            db_cursor.execute("""    
            SELECT
                prod.name AS product,
                prod.price AS price,
                store.name AS store
            FROM bangazon_api_product AS prod
            JOIN bangazon_api_store AS store
                ON prod.store_id = store.id
            WHERE price <= 1000
            """)
            
            #Pass the the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            #Convert flat data from dataset into a json-like datastructure
            products = []
            for row in dataset:
                
                #Create a dictionary that includes all required SQL columns
                product = {
                    'product': row['product'],
                    'price': row['price'],
                    'store': row['store']
                }
                #The append needs to be within the scope of the products dictionary or it will only load the last item in the list                
                products.append(product)
            
            # The template string must match the file name of the html template
            template = 'inexpensive_products.html'
        
            # The context will be a dictionary that the template can access to show data
            context = {
                "inexpensive_products_list": products
            }

            return render(request, template, context)