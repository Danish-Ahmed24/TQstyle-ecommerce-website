from decimal import Decimal

from .models import Category, ProductVariant


def base_context(request):
    """Inject globally-needed context into every template."""
    cart = request.session.get("cart", {})
    cart_count = sum(item["quantity"] for item in cart.values())

    cart_total = Decimal("0")
    if cart:
        variants = ProductVariant.objects.filter(
            id__in=cart.keys()
        ).values("id", "price")
        price_map = {str(v["id"]): v["price"] for v in variants}
        for vid, item in cart.items():
            if vid in price_map:
                cart_total += price_map[vid] * item["quantity"]

    # Wishlist — stored in session as a list of product IDs (ints)
    wishlist_ids = request.session.get("wishlist", [])

    return {
        "categories": Category.objects.all(),
        "cart_count": cart_count,
        "cart_total": cart_total,
        "wishlist_product_ids": set(wishlist_ids),
        "wishlist_count": len(wishlist_ids),
    }
