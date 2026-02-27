from urllib.parse import quote

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from app.cart import Cart
from app.forms import CheckoutForm
from app.models import Category, Customer, Order, OrderItem, Product, ProductVariant


def _is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


# --- Product views ---

def index(request):
    products = Product.objects.all()[:5]
    return render(request, "app/index.html", {
        "title": "Home",
        "products": products,
    })


def products(request):
    products = Product.objects.all()
    return render(request, "app/products.html", {
        "title": "Products",
        "products": products,
    })


def products_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, "app/products.html", {
        "title": category.name,
        "products": products,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "app/productDetail.html", {
        "title": product.name,
        "product": product,
    })


# --- Cart views ---

def cart_detail(request):
    cart = Cart(request)
    return render(request, "app/cart.html", {
        "title": "Your Cart",
        "cart": cart,
        "cart_total": cart.get_total_price(),
    })


def cart_add(request):
    if request.method != "POST":
        return redirect("cart")

    variant_id = request.POST.get("variant_id")
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if not variant.is_in_stock:
        if _is_ajax(request):
            return JsonResponse({"success": False, "message": "Out of stock"}, status=400)
        return redirect(request.POST.get("next", "cart"))

    quantity = max(1, int(request.POST.get("quantity", 1)))
    cart = Cart(request)
    cart.add(variant, quantity=quantity)

    if _is_ajax(request):
        return JsonResponse({
            "success": True,
            "message": "Added to cart",
            "cart_count": len(cart),
            "cart_total": str(cart.get_total_price()),
        })

    return redirect(request.POST.get("next", "cart"))


def cart_remove(request, variant_id):
    if request.method != "POST":
        return redirect("cart")

    cart = Cart(request)
    cart.remove(variant_id)

    if _is_ajax(request):
        return JsonResponse({
            "success": True,
            "removed": True,
            "cart_count": len(cart),
            "cart_total": str(cart.get_total_price()),
        })

    return redirect("cart")


def cart_update(request, variant_id):
    if request.method != "POST":
        return redirect("cart")

    quantity = int(request.POST.get("quantity", 1))
    cart = Cart(request)

    if quantity <= 0:
        cart.remove(variant_id)
        if _is_ajax(request):
            return JsonResponse({
                "success": True,
                "removed": True,
                "cart_count": len(cart),
                "cart_total": str(cart.get_total_price()),
            })
    else:
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart.add(variant, quantity=quantity, override_quantity=True)
        if _is_ajax(request):
            return JsonResponse({
                "success": True,
                "removed": False,
                "cart_count": len(cart),
                "cart_total": str(cart.get_total_price()),
                "item_total": str(variant.price * quantity),
            })

    return redirect("cart")


# --- Order / Checkout views ---

def checkout(request):
    """
    Unified checkout: collects customer details, saves the order, then either
    shows the order-success page (Place Order) or opens WhatsApp (WhatsApp order).
    """
    cart = Cart(request)
    items = list(cart)

    if not items:
        return redirect("cart")

    order_type = request.GET.get("order_type", "standard")  # used for initial GET

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order_type = cd.get("order_type", "standard")

            # Upsert Customer record (keyed by email)
            customer, _ = Customer.objects.get_or_create(
                email=cd["email"],
                defaults={
                    "name": cd["name"],
                    "phone": cd["phone"],
                    "address": cd["delivery_address"],
                },
            )
            # Always refresh phone / address / name in case they changed
            Customer.objects.filter(pk=customer.pk).update(
                name=cd["name"],
                phone=cd["phone"],
                address=cd["delivery_address"],
            )

            # Save order with customer snapshot + FK
            order = Order.objects.create(
                total_price=cart.get_total_price(),
                customer=customer,
                customer_name=cd["name"],
                customer_email=cd["email"],
                customer_phone=cd["phone"],
                delivery_address=cd["delivery_address"],
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    variant=item["variant"],
                    quantity=item["quantity"],
                    unit_price=item["variant"].price,
                )
            cart.clear()

            if order_type == "whatsapp":
                lines = [f"Hello! I'd like to place an order:\n"]
                for i, item in enumerate(items, 1):
                    variant = item["variant"]
                    lines.append(
                        f"{i}. {variant.product.name} (SKU: {variant.sku})"
                        f" x{item['quantity']} — Rs.{item['total_price']}"
                    )
                lines.append(f"\nTotal: Rs.{order.total_price}")
                lines.append(f"\nName: {cd['name']}")
                lines.append(f"Phone: {cd['phone']}")
                lines.append(f"Address: {cd['delivery_address']}")
                message = "\n".join(lines)
                number = getattr(settings, "WHATSAPP_NUMBER", "")
                return redirect(f"https://wa.me/{number}?text={quote(message)}")

            return redirect("order-success", order_id=order.id)
    else:
        form = CheckoutForm(initial={"order_type": order_type})

    return render(request, "app/checkout.html", {
        "title": "Checkout",
        "form": form,
        "cart": cart,
        "cart_total": cart.get_total_price(),
        "order_type": order_type,
    })


def order_success(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__variant__product"),
        id=order_id,
    )
    return render(request, "app/order_success.html", {
        "title": f"Order #{order.id} Confirmed",
        "order": order,
    })


# --- WhatsApp single-product order (from product page) ---

def whatsapp_order(request):
    """Add single variant to cart and redirect to WhatsApp checkout form."""
    if request.method != "POST":
        return redirect("index")

    variant_id = request.POST.get("variant_id")
    variant = get_object_or_404(ProductVariant, id=variant_id)
    quantity = max(1, int(request.POST.get("quantity", 1)))

    cart = Cart(request)
    cart.add(variant, quantity=quantity, override_quantity=False)

    return redirect(f"{request.build_absolute_uri('/checkout/')}?order_type=whatsapp")


# --- Wishlist views (session-based, no login required) ---

def wishlist_toggle(request, product_id):
    """Toggle a product in/out of the session wishlist. Returns JSON for AJAX."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    wishlist = request.session.get("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        wishlisted = False
    else:
        wishlist.append(product_id)
        wishlisted = True

    request.session["wishlist"] = wishlist
    request.session.modified = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"wishlisted": wishlisted, "count": len(wishlist)})

    return redirect(request.META.get("HTTP_REFERER", "products"))


def wishlist_page(request):
    """Show all wishlisted products."""
    wishlist = request.session.get("wishlist", [])
    products = Product.objects.filter(id__in=wishlist)
    return render(request, "app/wishlist.html", {
        "title": "Wishlist",
        "products": products,
    })
