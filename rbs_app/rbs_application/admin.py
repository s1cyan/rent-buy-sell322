from django.contrib import admin
from .models import *

# Register your models here.

myModels = [
    Category,
    Comment,
    Complaint,
    Order,
    Product,
    Rating,
    ShoppingCart,
    UserProfile,
]  # iterable list
admin.site.register(myModels)
