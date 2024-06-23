from django.contrib import admin

from .models import (
    Product,
    PreCategory,
    Category,
    Vendor,
    ProductImages,
    ProductInfo,
    Tag,
    ProductReview,
    Whishlist,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductInfo(admin.TabularInline):
    model = ProductInfo


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, ProductInfo]
    list_display = [
        "title",
        "category",
        "product_image",
        "price",
        "featured",
        "product_status",
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category_image"]


class PreCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category_image"]


class VendorAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]


class CartOrderAdmin(admin.ModelAdmin):
    list_display = ["user", "price", "paid_status", "order_date", "product_status"]


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "item", "invoice_no", "image", "qty", "price", "total"]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "review", "rating"]


class WhishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "date"]


class CartItemsAdmin(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemsAdmin]


class OrderItemsAdmin(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsAdmin]


admin.site.register(Product, ProductAdmin)
admin.site.register(PreCategory, PreCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Whishlist, WhishlistAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tag)
