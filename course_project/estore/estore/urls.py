from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from estore.apps.account.admin import staff_admin_site

urlpatterns = [
    path("estore-admin/", admin.site.urls),
    path("staff-admin/", staff_admin_site.urls),
    path("", include("estore.apps.catalogue.urls", namespace="catalogue")),
    path("checkout/", include("estore.apps.checkout.urls", namespace="checkout")),
    path("basket/", include("estore.apps.basket.urls", namespace="basket")),
    path("account/", include("estore.apps.account.urls", namespace="account")),
    path("orders/", include("estore.apps.orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
