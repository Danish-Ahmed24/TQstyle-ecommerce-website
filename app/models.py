from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="EMPTY")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    #variants will be handled in a separate model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_variants = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    values = models.ManyToManyField('Value')
    @property
    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        return f"{self.product.name} (#{self.id})"

class Attribute(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Value(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)
    class Meta:
        unique_together = ['attribute', 'value']

    def __str__(self): 
        return f"{self.attribute.name}: {self.value}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='categories/')
    def __str__(self):
        return self.name