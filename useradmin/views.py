import datetime
from django.shortcuts import render, redirect
from core.models import Order, Product, Category
from django.db.models import Sum
from .forms import ProductForm, ProductEditForm
from userauths.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def dashboard(request):
    # Получение данных о доходе, количестве заказов и т.д.
    revenue = Order.objects.aggregate(total_price=Sum("total_price"))
    total_orders_count = Order.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")[:6]
    latest_orders = Order.objects.all()

    this_month = datetime.datetime.now().month
    monthly_revenue = Order.objects.filter(created__month=this_month).aggregate(
        total_price=Sum("total_price")
    )

    # Поиск по номеру телефона
    phone_number = request.GET.get("phone_number")
    if phone_number:
        latest_orders = latest_orders.filter(phone=phone_number)

    # Пагинация
    paginator = Paginator(latest_orders, 10)  # Показывать по 10 заказов на странице
    page = request.GET.get("page")
    try:
        latest_orders = paginator.page(page)
    except PageNotAnInteger:
        latest_orders = paginator.page(1)
    except EmptyPage:
        latest_orders = paginator.page(paginator.num_pages)

    context = {
        "monthly_revenue": monthly_revenue,
        "revenue": revenue,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "total_orders_count": total_orders_count,
        "phone_number": phone_number,  # Передаем значение телефона обратно в шаблон
    }
    return render(request, "useradmin/dashboard.html", context)


def dashboard_products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()

    # Обработка фильтрации по категориям
    category_filter = request.GET.get("category")
    if category_filter:
        all_products = all_products.filter(category=category_filter)

    # Пагинация
    paginator = Paginator(all_products, 20)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если номер страницы не является целым числом, отображаем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем доступно страниц, отображаем последнюю страницу
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "all_categories": all_categories,
    }
    return render(request, "useradmin/dashboard-products.html", context)


def dashboard_edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    status = product.product_status
    character = product.product_character
    print(status, character)

    if request.method == "POST":
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.product_character = character
            new_form.product_status = status
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard-products")
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product,
    }
    return render(request, "useradmin/dashboard-edit-products.html", context)


def dashboard_delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:dashboard-products")
