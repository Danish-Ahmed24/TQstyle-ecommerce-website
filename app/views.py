from django.http import JsonResponse
from django.shortcuts import render
from app.forms import ProductForm
from app.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()

    return render(request, "app/index.html", {
        "title": "Home",
        "products": products
        })

