from .models import Category
from ..account.models import Address


def categories(request):
    return {"categories": Category.objects.filter(level=0)}


def delivery_addresses(request):
    addresses = Address.objects.all()
    return {"addresses": addresses}
