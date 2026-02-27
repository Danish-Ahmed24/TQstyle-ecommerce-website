from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:id>/", views.product_detail, name="product-detail"),
    path("products/", views.products, name="products"),
    path("products/<int:category_id>/", views.products_category, name="products-by-category"),

    # Cart
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/", views.cart_add, name="cart-add"),
    path("cart/remove/<int:variant_id>/", views.cart_remove, name="cart-remove"),
    path("cart/update/<int:variant_id>/", views.cart_update, name="cart-update"),

    # Orders / Checkout
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/", views.order_success, name="order-success"),

    # WhatsApp single-product order (from product page)
    path("cart/whatsapp-order/", views.whatsapp_order, name="whatsapp-order"),

    # Wishlist (session-based)
    path("wishlist/", views.wishlist_page, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.wishlist_toggle, name="wishlist-toggle"),
]
