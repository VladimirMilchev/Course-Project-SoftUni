from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('estore.store.urls', namespace='estore')),
    path('basket/', include('estore.basket.urls', namespace='basket')),
    path('payment/', include('estore.payment.urls', namespace='payment')),
    path('account/', include('estore.account.urls', namespace='account')),
    path('orders/', include('estore.orders.urls', namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
