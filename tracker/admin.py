from django.contrib import admin
from tracker.models import Category, Transaction

# Register your models here.

admin.site.register(Transaction)  # Registering the Transaction model
admin.site.register(Category)  # Registering the Category model
