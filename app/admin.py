from django.contrib import admin
from .models import Attribute, Category, Product, ProductVariant, Value

# Register your models here.
admin.site.site_header = "TQstyle Admin"
admin.site.site_title = "TQstyle Admin Portal"
admin.site.index_title = "Welcome to TQstyle Admin Portal"
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Attribute)
admin.site.register(Value)
admin.site.register(Category)

# Category Product banate waqt hi 