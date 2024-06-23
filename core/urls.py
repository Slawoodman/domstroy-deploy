from django import views
from django.urls import path, include
from core.views import (
    ajax_quick_product_detail_view,
    filter_data,
    add_to_wishlist,
    ajax_add_review,
    cart_view,
    category_list_view,
    precategory_list_view,
    category_product_list__view,
    checkout_view,
    customer_dashboard,
    delete_item_from_cart,
    filter_product,
    index,
    order_detail,
    product_detail_view,
    product_list_page_view,
    remove_wishlist,
    search_view,
    update_cart,
    wishlist_view,
    contact,
    about_us,
    purchase_guide,
    privacy_policy,
    terms_of_service,
    precategory_product_list__view,
    AddToCartView,
    create_order,
    filter_products_view,
)

app_name = "core"

urlpatterns = [
    # Homepage
    path("", index, name="index"),
    path("products/", product_list_page_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
    path("filter_products/", filter_products_view, name="filter-products"),
    path(
        "ajax/quick-product-detail/<str:pid>/",
        ajax_quick_product_detail_view,
        name="ajax_quick_product_detail",
    ),
    path("filter-data", filter_data, name="filter_data"),
    # Category
    path("category/", category_list_view, name="category-list"),
    path(
        "category/<str:cid>/subcategories/",
        precategory_list_view,
        name="precategory-list",
    ),
    path("category/<cid>/", category_product_list__view, name="category-product-list"),
    path(
        "category/subcategories/<str:pid>",
        precategory_product_list__view,
        name="subcategory-product-list",
    ),
    # Add Review
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),
    # Search
    path("search/", search_view, name="search"),
    # Filter product URL
    path("filter-products/", filter_product, name="filter-product"),
    # Add to cart URL
    path("add-item/<str:id>", AddToCartView.as_view(), name="add-to-cart"),
    # Cart Page URL
    path("cart/", cart_view, name="cart"),
    # Delete ITem from Cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    # Update  Cart
    path("update-cart/", update_cart, name="update-cart"),
    # Checkout  URL
    path("checkout/", checkout_view, name="checkout"),
    path("create-order/", create_order, name="create_order"),
    # Dahboard URL
    path("dashboard/", customer_dashboard, name="dashboard"),
    # Order Detail URL
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),
    # wishlist page
    path("wishlist/", wishlist_view, name="wishlist"),
    # adding to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),
    # Remvoing from wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),
    path("contact/", contact, name="contact"),
    path("about_us/", about_us, name="about_us"),
    path("purchase_guide/", purchase_guide, name="purchase_guide"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("terms_of_service/", terms_of_service, name="terms_of_service"),
]
