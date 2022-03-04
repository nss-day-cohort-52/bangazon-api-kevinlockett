from django.urls import path
from .views import (ExpensiveProducts)

urlpatterns = [
    path('expensiveproducts', ExpensiveProducts.as_view())
]
