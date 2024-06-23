from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from core.models import (
    Product,
    Category,
    Vendor,
    Cart,
    CartItem,
    ProductImages,
    ProductReview,
    Whishlist,
    PreCategory,
    Order,
    OrderItem,
    Tag,
)
from userauths.models import Profile
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View
import calendar
import json
from django.db.models import Count, Avg, Min, Max
from django.db.models.functions import ExtractMonth
from . import utils


def index(request):
    products = Product.objects.filter(
        product_status="published", featured=True
    ).order_by("-id")
    context = {
        "products": products,
        "new_prod_count": products.filter(product_character="NEW").count(),
        "old_prod_count": products.filter(product_character="USED").count(),
    }

    return render(request, "core/index.html", context)


@csrf_exempt
def filter_data(request):
    print(request.POST)
    if request.POST:
        category = request.POST.get("category_id")
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        product_status = request.POST.get("product_status")

        # Base queryset
        all_products = Product.objects.all().order_by("-id")

        # Apply category filter
        if category != "all":
            all_products = all_products.filter(category_id=category)

        # Apply price range filter
        if min_price and max_price:
            if max_price > min_price:
                all_products = all_products.filter(price__range=(min_price, max_price))

        # Apply product status filter
        if product_status:
            all_products = all_products.filter(product_character=product_status.upper())

        t = render_to_string(
            "core/async/product-index.html", {"products": all_products}
        )
        return JsonResponse({"data": t})
    else:
        # Default queryset
        all_products = Product.objects.filter(
            product_status="published", featured=True
        ).order_by("-id")
        t = render_to_string(
            "core/async/product-index.html", {"products": all_products}
        )
        return JsonResponse({"data": t})


def product_list_page_view(request):
    tags = Tag.objects.all()
    products = Product.objects.all()
    min_max_price = products.aggregate(Min("price"), Max("price"))
    print(min_max_price)
    context = {
        "products": products,
        "sort_by": "",
        "total_count": products.count(),
        "sort_title": "Назвою",
        "min_max_price": min_max_price,
        "tags": tags,
    }
    return render(request, "core/product-list.html", context)


def filter_products_view(request):
    print(request.POST)
    sort_by = request.POST.get("sort_by", "name")
    min_price = request.POST.get("min_price")
    max_price = request.POST.get("max_price")
    category_ids = request.POST.getlist("category")
    vendor_ids = request.POST.getlist("vendor")
    tags = request.POST.getlist("tag")

    products = Product.objects.all()

    # Filter by category
    if category_ids:
        products = products.filter(category__id__in=category_ids)

    # Filter by vendor
    if vendor_ids:
        products = products.filter(vendor__id__in=vendor_ids).distinct()
        print(f"Сортировка за {vendor_ids} : {products}")

    # Filter by tags
    if tags:
        products = products.filter(tags__name__in=tags).distinct()

    # Filter by price
    if min_price and max_price:
        products = products.filter(price__range=(min_price, max_price))
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    if sort_by:
        if sort_by == "price_asc":
            products = products.order_by("price")
        elif sort_by == "price_desc":
            products = products.order_by("-price")
        elif sort_by == "release_date":
            products = products.order_by("-date")
        elif sort_by == "rating":
            products = products.annotate(
                average_rating=Avg("reviews__rating")
            ).order_by("-average_rating")
        else:
            products = products.order_by("title")

    # Render HTML for filtered products
    html = render_to_string("core/async/product-list.html", {"products": products})

    return JsonResponse({"html": html})


def category_list_view(request):
    data = Category.objects.all()
    categ, custom_range = utils.Paginate(request, data, 6)

    context = {"categ": categ, "custom_range": custom_range}
    return render(request, "core/category-list.html", context)


def precategory_list_view(request, cid):
    category = Category.objects.get(cid=cid)

    # Filter PreCategory objects by the category
    data = PreCategory.objects.filter(category=category)
    precatlst, custom_range = utils.Paginate(request, data, 6)

    context = {
        "categ": precatlst,
        "custom_range": custom_range,
        "page": f"{category}",
        "ctn": len(data),
    }
    return render(request, "core/category-list.html", context)


def category_product_list__view(request, cid):

    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    products, custom_range = utils.Paginate(request, products, 6)
    total_count = len(products)

    context = {
        "category": category,
        "products": products,
        "custom_range": custom_range,
        "total_count": total_count,
    }
    return render(request, "core/category-product-list.html", context)


def precategory_product_list__view(request, pid):

    precategory = PreCategory.objects.get(pid=pid)
    products = Product.objects.filter(
        product_status="published", precategory=precategory
    )
    total_count = len(products)
    products, custom_range = utils.Paginate(request, products, 2)

    context = {
        "category": precategory,
        "products": products,
        "custom_range": custom_range,
        "total_count": total_count,
    }
    return render(request, "core/category-product-list.html", context)


def get_rating_percentages(product):
    total_reviews = ProductReview.objects.filter(product=product).count()
    rating_percentages = (
        ProductReview.objects.filter(product=product)
        .values("rating")
        .annotate(percentage=Count("rating") * 100 / total_reviews)
        .order_by("rating")
    )
    reversed_percentages = list(
        reversed(
            [
                (f'{rating["rating"]} star', round(rating["percentage"], 2))
                for rating in rating_percentages
            ]
        )
    )

    # Преобразуем обратный список кортежей обратно в словарь
    return dict(reversed_percentages)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    recently_added = Product.objects.all().order_by("-date")[:3]

    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    rating_percentages = get_rating_percentages(
        product
    )  # Получаем количество отзывов для каждой оценки

    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product
        ).count()

        if user_review_count > 0:
            make_review = False

    p_image = product.p_images.all()

    context = {
        "p": product,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
        "recently_added": recently_added,
        "rating_percentages": rating_percentages,  # Добавляем в контекст количество отзывов для каждой оценки
    }
    print(context["rating_percentages"])
    return render(request, "core/product-detail.html", context)


@csrf_exempt
def ajax_quick_product_detail_view(request, pid):
    if request.method == "GET":
        pid = request.GET.get(
            "product_id"
        )  # Получаем айдишник продукта из POST-запроса
        print(pid)
        try:
            product = Product.objects.get(pid=pid)
            product_images = product.p_images.all()
            print(product_images)
            context = {"product": product, "product_images": product_images}
            html_content = render_to_string("core/async/quickViewModal.html", context)
            return JsonResponse({"html_content": html_content})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    context = {
        "user": user.username,
        "review": request.POST["review"],
        "rating": request.POST["rating"],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    return JsonResponse(
        {"bool": True, "context": context, "average_reviews": average_reviews}
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")
    precatlst, custom_range = utils.Paginate(request, products, 10)

    context = {
        "query": query,
        "products": precatlst,
        "custom_range": custom_range,
    }
    return render(request, "core/search.html", context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET["min_price"]
    max_price = request.GET["max_price"]

    products = (
        Product.objects.filter(product_status="published").order_by("-id").distinct()
    )

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})


class AddToCartView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.GET.get("quantity"))
        print(quantity)
        quantity = int(request.GET.get("quantity"))
        print(quantity)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(
            request,
            f'Товар "{product.title}" успішно доданий до кошику. Кількість: {cart_item.quantity}',
        )
        # Return a JSON response for AJAX request
        if request.is_ajax():
            return JsonResponse(
                {
                    "success": True,
                    "message": f'Товар "{product.title}" успішно доданий до кошику. Кількість: {cart_item.quantity}',
                }
            )

        # Fallback for non-AJAX request

        return redirect("index")


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    try:
        cartitems = cart.items.all()
        print(cartitems)
        total_price = sum(
            [item.quantity * item.product.price for item in cart.items.all()]
        )
        return render(
            request,
            "core/cart.html",
            {"cart": cart, "total_price": total_price, "cartitems": cartitems},
        )
    except:
        messages.warning(request, "Ваш кошик порожній")
        return redirect("core:index")


def delete_item_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if product_id:
            cart_item = get_object_or_404(CartItem, id=product_id)
            if cart_item:
                cart_item.delete()
                cart = cart_item.cart
                total_price = sum(item.price_sum for item in cart.items.all())
                total_items = sum(item.quantity for item in cart.items.all())
                cart_items = CartItem.objects.filter(cart=cart)
                context = {
                    "cartitems": cart_items,
                    "total_price": total_price,
                    "total_items": total_items,
                }
                cart_html = render_to_string("core/async/cart-list.html", context)
                return JsonResponse(
                    {
                        "data": cart_html,
                        "success": True,
                        "total_price": total_price,
                        "total_items": total_items,
                    }
                )
            else:
                return JsonResponse(
                    {"error": "Товар не знайдено в корзині."}, status=400
                )
        else:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            total_price = 0
            total_items = 0
            context = {
                "cartitems": [],
                "success": True,
                "total_price": total_price,
                "total_items": total_items,
            }
            cart_html = render_to_string("core/async/cart-list.html", context)
            return JsonResponse(
                {
                    "data": cart_html,
                    "success": True,
                    "total_price": total_price,
                    "total_items": total_items,
                }
            )
    else:
        return JsonResponse({"error": "Метод запиту не дозволений."}, status=405)


def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get("item_id")
        new_quantity = data.get("quantity")
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.quantity = new_quantity
            cart_item.price_sum = cart_item.quantity * cart_item.product.price
            cart_item.save()

            cart = cart_item.cart
            for item in cart.items.all():
                item.price_sum = item.product.price * item.quantity
                item.save()

            # Вычисляем общую стоимость заказа и общее количество товаров
            total_price = sum([item.price_sum for item in cart.items.all()])
            total_items = sum([item.quantity for item in cart.items.all()])

            # Обновляем HTML-контент корзины
            cart_html = render_to_string(
                "core/async/cart-list.html",
                {"cartitems": cart.items.all(), "total_price": total_price},
            )

            print(cart_html)

            return JsonResponse(
                {
                    "success": True,
                    "cart_html": cart_html,
                }
            )

        except CartItem.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Одиницю товару не знайденно"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"success": False, "error": "Не достпуний метод"})


@login_required
def checkout_view(request):
    context = {}
    cart = Cart.objects.get(user=request.user)
    cartitems = cart.items.all()
    total_price = sum([item.quantity * item.product.price for item in cart.items.all()])
    context["cartitems"] = cartitems
    context["total_price"] = total_price

    return render(request, "core/checkout.html", context)


@login_required
def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fname = data.get("fname")
        phone = data.get("phone")
        billing_address = data.get("billing_address")
        payment_option = data.get("payment_option")

        # Создание заказа
        # Create Order instance
        order = Order.objects.create(
            customer=request.user,
            address=billing_address,
            phone=phone,
            payment_method=payment_option,
            total_price=0,  # Initialize total price
        )

        # Add items to the order
        cart = Cart.objects.get(user=request.user)
        cartitems = cart.items.all()
        total_price = 0
        for item in cartitems:
            order_item = OrderItem.objects.create(
                order_of_item=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price * item.quantity,
            )
            total_price += item.quantity * item.product.price

        # Update the order total price
        order.total_price = total_price
        order.save()

        # Clear the cart after creating the order
        cart.items.all().delete()

        messages.success(request, "Замовлення успішно відправленно на обробку!")
        return redirect(
            "core:dashboard"
        )  # Redirect to the dashboard on successful order creation
    else:
        messages.error(request, "Спробуйте ще раз, щось пішло не так.")
        return redirect("core:checkout")  # Redirect to the checkout page on error


@login_required
def customer_dashboard(request):
    orders_list = Order.objects.filter(customer=request.user).order_by("-id")

    orders = (
        Order.objects.annotate(month=ExtractMonth("created"))
        .values("month")
        .annotate(count=Count("id"))
        .values("month", "count")
    )
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    user_profile = Profile.objects.get(user=request.user)

    context = {
        "user_profile": user_profile,
        "orders": orders,
        "orders_list": orders_list,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def order_detail(request, id):
    order = Order.objects.get(customer=request.user, id=id)
    order_items = order.order_items.all()

    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(request, "core/order-detail.html", context)


@login_required
def wishlist_view(request):
    wishlist = Whishlist.objects.filter(user=request.user)
    wishlist = Whishlist.objects.filter(user=request.user)
    context = {"w": wishlist}
    return render(request, "core/wishlist.html", context)


@login_required
def add_to_wishlist(request):
    if request.user.is_authenticated:
        product_id = request.GET.get("id")
        product = Product.objects.get(id=product_id)
        wishlist_count = Whishlist.objects.filter(
            product=product, user=request.user
        ).count()
        if wishlist_count > 0:
            messages.error(request, "Товар вже в  бажаному")
        else:
            new_wishlist = Whishlist.objects.create(
                user=request.user,
                product=product,
            )
            messages.success(request, "Товар доданий в  бажане")
        return JsonResponse({"success": True})
    else:
        return redirect("userauths:sign-in")  # Перенаправление на страницу входа


def remove_wishlist(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        if request.user.is_authenticated:
            wishlist_item_id = request.POST.get("wishlist_item_id")
            try:
                wishlist_item = Whishlist.objects.get(
                    id=wishlist_item_id, user=request.user
                )
                wishlist_item.delete()
                wishlist = Whishlist.objects.filter(user=request.user)
                context = {"w": wishlist}
                html = render_to_string("core/async/wishlist-list.html", context)
                return JsonResponse({"data": html, "success": True})
            except Whishlist.DoesNotExist:
                return JsonResponse(
                    {"error": "Товар зі списку не знайденно.", "success": False}
                )
            except Exception as e:
                return JsonResponse({"error": str(e), "success": False})
        else:
            return JsonResponse({"error": "Невірний запит.", "success": False})


def contact(request):
    return render(request, "core/contact.html")


def about_us(request):
    return render(request, "core/about_us.html")


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def terms_of_service(request):
    return render(request, "core/terms_of_service.html")
