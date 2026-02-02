from django.shortcuts import render
from app.models import Category, Product

# Create your views here.
def index(request):
    products = Product.objects.all()[:5]
    categorys = Category.objects.all()
    return render(request, "app/index.html", {
        "title": "Home",
        "products": products,
        "categorys": categorys
        })

def products(request):
    products = Product.objects.all()
    categorys = Category.objects.all()
    return render(request, "app/products.html", {
        "title": "Products",
        "products": products,
        "categorys": categorys
        })