from django.contrib import admin
from ecomm_app.models import Products

# Register your models here.
from ecomm_app.models import Products

# admin.site.register(Products)

class ProductsAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','cat','is_active']
    list_filter=['cat','is_active']

admin.site.register(Products,ProductsAdmin)