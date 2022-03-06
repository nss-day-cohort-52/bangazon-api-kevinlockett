from django.urls import path
from .views import (CompletedOrders, ExpensiveProducts, FavoritedSellersByCustomer, InexpensiveProducts, IncompleteOrders)

urlpatterns = [
    path('completedorders', CompletedOrders.as_view()),
    path('expensiveproducts', ExpensiveProducts.as_view()),
    path('favoritedsellersbycustomer', FavoritedSellersByCustomer.as_view()),
    path('incompleteorders', IncompleteOrders.as_view()),
    path('inexpensiveproducts', InexpensiveProducts.as_view())
]
