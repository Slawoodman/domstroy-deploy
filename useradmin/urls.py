from django.urls import path
from useradmin import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "useradmin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.dashboard_products, name="dashboard-products"),
    path(
        "edit-products/<pid>/",
        views.dashboard_edit_product,
        name="dashboard-edit-products",
    ),
    path(
        "delete-products/<pid>/",
        views.dashboard_delete_product,
        name="dashboard-delete-products",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
