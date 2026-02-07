from django.db import models

# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.IntegerField()
#     images = models.ImageField(upload_to='products/')
#     category = models.ForeignKey('Category', on_delete=models.CASCADE,related_name='products')   

#     def __str__(self):
#         return self.name    

# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     #products
#     def __str__(self):
#         return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="EMPTY")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='products/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    related_products = models.ManyToManyField('self', blank=True)
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='categories/')
    def __str__(self):
        return self.name