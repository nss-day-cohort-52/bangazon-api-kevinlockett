from django.urls import path
from .views import (ExpensiveProducts, InexpensiveProducts )

urlpatterns = [
    path('expensiveproducts', ExpensiveProducts.as_view()),
    path('inexpensiveproducts', InexpensiveProducts.as_view())
]
