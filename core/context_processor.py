from ast import Add
from core.models import Product, Category, Vendor, Cart, Whishlist
from django.db.models import Min, Max
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    wishlist = 0
    cart_items = []

    if request.user.is_authenticated:
        wishlist = Whishlist.objects.filter(user=request.user)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = Cart.objects.get(user=request.user).items.all()
    else:
        wishlist = 0
        cart_items = []

    categories_per_sublist = 2
    sublists = [
        categories[i : i + categories_per_sublist]
        for i in range(0, len(categories), categories_per_sublist)
    ]

    return {
        "categories": categories,
        "cat_meny": sublists,
        "wishlist": wishlist,
        "cart_items": cart_items,
        "vendors": vendors,
        "min_max_price": min_max_price,
    }
