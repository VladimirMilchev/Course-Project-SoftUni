from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .forms import ProductSearchForm
from .models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = "catalogue/index.html"
    context_object_name = "products"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).prefetch_related("product_image")


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True)
    )
    return render(request, "catalogue/category.html", {"category": category, "products": products})


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalogue/single.html"
    context_object_name = "product"
    queryset = Product.objects.filter(is_active=True)
    slug_field = "slug"


def search_products(request):
    search_form = ProductSearchForm(request.POST)
    results = []

    if search_form.is_valid():
        search_query = search_form.cleaned_data['search_query']
        results = Product.objects.filter(title__icontains=search_query)

    return render(request, 'catalogue/search_results.html', {'results': results})
