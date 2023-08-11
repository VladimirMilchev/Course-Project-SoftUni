from django.urls import path

from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="store_home"),
    path("<slug:slug>", views.ProductDetailView.as_view(), name="product_detail"),
    path("shop/<slug:category_slug>/", views.category_list, name="category_list"),
    path('search/', views.search_products, name='search_products'),
]
