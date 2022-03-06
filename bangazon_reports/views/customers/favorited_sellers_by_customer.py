"""Module for generating Expensive Products Report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class FavoritedSellersByCustomer(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            #Execute SQLite3 query:
            db_cursor.execute("""    
            SELECT
                user.id AS customer_id,
                ( user.first_name || " " || user.last_name ) AS customer,
                store.name AS store
            FROM bangazon_api_favorite AS fav
            JOIN auth_user AS user
                ON fav.customer_id = user.id
            JOIN bangazon_api_store AS store
                ON fav.store_id = store.id
            """)
            
            #Pass the the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            #Convert flat data from dataset into a json-like datastructure
            stores_by_customer = []
            
            for row in dataset:
                
                #Create a dictionary that includes all required SQL columns
                
                store = {
                    'store': row['store']
                }
                
                #This is using a generator comprehension to find the user_dict in the favorited_stores_by_user
                # The next function grabs the dictionary at the beginning of the generator
                # If the generator is empty it returns None
                cust_dict = next(
                    (
                        cust_store for cust_store in stores_by_customer
                        if cust_store['customer_id'] == row['customer_id']
                    ),
                    None
                )
                
                # If the cust_dict is already in the favorited_sellers_by_customer list, append the store to the stores list
                if cust_dict:
                    cust_dict['stores'].append(store)
                else:
                    # If the user is not on the stores_by_user list, create and add the user to the list
                    stores_by_customer.append({
                        'customer_id': row['customer_id'],
                        'customer': row['customer'],
                        'stores': [store]
                    })
                    
            # The template string must match the file name of the html template
            template = 'favorited_sellers_by_customer.html'
        
            # The context will be a dictionary that the template can access to show data
            context = {
                "favorited_sellers_by_customer_list": stores_by_customer
            }

            return render(request, template, context)