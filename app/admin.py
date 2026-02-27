from django.contrib import admin

from .models import Attribute, Category, Customer, Order, OrderItem, Product, ProductVariant, Value

# ─── Site branding ───────────────────────────────────────────
admin.site.site_header = "TQstyle Admin"
admin.site.site_title  = "TQstyle Admin Portal"
admin.site.index_title = "Welcome to TQstyle Admin Portal"


# ─── Inlines ─────────────────────────────────────────────────

class ValueInline(admin.TabularInline):
    """Edit all values (e.g. Gold, Silver) right inside the Attribute form."""
    model  = Value
    extra  = 2
    fields = ('value',)


class ProductVariantInline(admin.StackedInline):
    """Add / edit variants directly on the Product page — no separate URL needed."""
    model       = ProductVariant
    extra       = 1
    fields      = ('image', 'price', 'stock', 'sku', 'values')
    filter_horizontal = ('values',)
    show_change_link  = True


class CustomerOrderInline(admin.TabularInline):
    """Show all orders for a customer without leaving the Customer page."""
    model           = Order
    extra           = 0
    can_delete      = False
    show_change_link = True
    readonly_fields = ('id', 'status', 'total_price', 'created_at')
    fields          = ('id', 'status', 'total_price', 'created_at')
    ordering        = ('-created_at',)


class OrderItemInline(admin.TabularInline):
    """See every line item inside an Order without leaving the page."""
    model               = OrderItem
    extra               = 0
    readonly_fields     = ('variant', 'quantity', 'unit_price', 'total_price_display')
    fields              = ('variant', 'quantity', 'unit_price', 'total_price_display')
    can_delete          = False

    def total_price_display(self, obj):
        total = obj.total_price
        if total is None:
            return "-"
        return f"Rs. {total:,.2f}"
    total_price_display.short_description = "Line total"


# ─── ModelAdmins ─────────────────────────────────────────────

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display    = ('name', 'email', 'phone', 'order_count', 'created_at')
    search_fields   = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'order_count')
    inlines         = [CustomerOrderInline]

    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'phone', 'address'),
        }),
        ('Notes', {
            'fields': ('notes',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def order_count(self, obj):
        return obj.orders.count()
    order_count.short_description = "Orders"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)
    inlines       = [ValueInline]


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display  = ('attribute', 'value')
    list_filter   = ('attribute',)
    search_fields = ('value', 'attribute__name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display    = ('name', 'category', 'variant_count', 'created_at')
    list_filter     = ('category',)
    search_fields   = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines         = [ProductVariantInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def variant_count(self, obj):
        return obj.variants.count()
    variant_count.short_description = "Variants"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display       = ('__str__', 'sku', 'price', 'stock', 'is_in_stock')
    list_filter        = ('product__category',)
    search_fields      = ('sku', 'product__name')
    readonly_fields    = ('sku',)
    filter_horizontal  = ('values',)

    def is_in_stock(self, obj):
        return obj.is_in_stock
    is_in_stock.boolean = True
    is_in_stock.short_description = "In stock?"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('id', 'customer_name', 'customer_phone', 'status', 'total_price', 'created_at')
    list_filter     = ('status',)
    search_fields   = ('customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('created_at', 'total_price')
    inlines         = [OrderItemInline]

    fieldsets = (
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'delivery_address'),
        }),
        ('Order Info', {
            'fields': ('status', 'total_price', 'created_at'),
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'variant', 'quantity', 'unit_price')
    readonly_fields = ('order', 'variant', 'quantity', 'unit_price')
