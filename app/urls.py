from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    # index.html
    path("",views.index,name="index"),
    
    # productDetail.html
    path("product/<int:id>/", views.product_detail, name="product-detail"),
    
    # products.html
    path("products/",views.products,name="products"),
    path('products/<int:category_id>/', views.products_category, name='products-by-category'),

]

urlpatterns += staticfiles_urlpatterns()
