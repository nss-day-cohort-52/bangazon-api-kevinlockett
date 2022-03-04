from django.urls import path
from .views import (CompletedOrders, ExpensiveProducts, InexpensiveProducts )

urlpatterns = [
    path('expensiveproducts', ExpensiveProducts.as_view()),
    path('inexpensiveproducts', InexpensiveProducts.as_view()),
    path('completedorders', CompletedOrders.as_view())
]
