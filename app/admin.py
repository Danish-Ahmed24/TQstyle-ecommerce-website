from django.contrib import admin
from .models import Category, Product

# Register your models here.
admin.site.site_header = "TQstyle Admin"
admin.site.site_title = "TQstyle Admin Portal"
admin.site.index_title = "Welcome to TQstyle Admin Portal"
admin.site.register(Product)
admin.site.register(Category)