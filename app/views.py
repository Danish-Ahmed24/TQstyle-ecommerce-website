from django.shortcuts import render, get_object_or_404
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

def products_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categorys = Category.objects.all()
    return render(request, "app/products.html", {
        "title": "Products",
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

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "app/productDetail.html", {
        "title": product.name,
        "product": product,
        })