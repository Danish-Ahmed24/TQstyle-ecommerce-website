from decimal import Decimal
from .models import ProductVariant


class Cart:
    """Session-based shopping cart.

    Cart data in session:
        {
            "<variant_id>": {"quantity": <int>, "product_id": <int>},
            ...
        }
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if cart is None:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, variant, quantity=1, override_quantity=False):
        """Add a variant to the cart or increment its quantity.

        Args:
            variant: ProductVariant instance.
            quantity: Number of units to add (or set when override_quantity=True).
            override_quantity: Replace current quantity instead of incrementing.
        """
        vid = str(variant.id)
        if vid not in self.cart:
            self.cart[vid] = {"quantity": 0, "product_id": variant.product_id}
        if override_quantity:
            self.cart[vid]["quantity"] = quantity
        else:
            self.cart[vid]["quantity"] += quantity
        self._save()

    def remove(self, variant_id):
        """Remove a variant from the cart entirely."""
        vid = str(variant_id)
        if vid in self.cart:
            del self.cart[vid]
            self._save()

    def _save(self):
        self.session.modified = True

    def __iter__(self):
        """Yield enriched cart items with variant ORM objects and line totals."""
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(
            id__in=variant_ids
        ).select_related("product")
        variant_map = {str(v.id): v for v in variants}

        for vid, item in self.cart.items():
            if vid not in variant_map:
                # Variant was deleted from DB; skip silently
                continue
            variant = variant_map[vid]
            yield {
                "variant": variant,
                "quantity": item["quantity"],
                "total_price": variant.price * item["quantity"],
            }

    def __len__(self):
        """Total unit count across all line items."""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Sum of all line totals."""
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids)
        variant_map = {str(v.id): v for v in variants}
        total = Decimal("0")
        for vid, item in self.cart.items():
            if vid in variant_map:
                total += variant_map[vid].price * item["quantity"]
        return total

    def clear(self):
        """Remove the cart from the session."""
        self.session.pop("cart", None)
        self._save()
