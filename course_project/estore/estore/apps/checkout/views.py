import json
import secrets
from urllib.parse import urlparse, parse_qs

import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from estore.apps.account.models import Address
from estore.apps.basket.basket import Basket
from estore.apps.orders.models import Order, OrderItem

from .models import DeliveryOptions

from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient
from ..catalogue.models import Product


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if addresses.exists():
        if "address" not in session:
            session["address"] = {"address_id": str(addresses[0].id)}
        else:
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})


####
# PayPay
####


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful_stripe(request):
    basket = Basket(request)
    user_email = request.user.email
    current_url = request.build_absolute_uri()
    parsed_url = urlparse(current_url)
    query_params = parse_qs(parsed_url.query)
    if 'token' in query_params:
        token_value = query_params['token'][0]
    try:
        order = Order.objects.get(email=user_email, order_key=token_value, billing_status=False)
        order.billing_status = True
        order.save()
        basket.clear()
    except Order.DoesNotExist:
        pass

    return render(request, "checkout/payment_successful.html", {})


@login_required
def create_checkout_session(request):
    token = secrets.token_hex(16)
    basket = Basket(request)
    total = basket.get_total_price()

    YOUR_DOMAIN = "http://localhost:8000"

    try:
        stripe.api_key = 'sk_test_51NVYMbLyAg8eICZpo2eVo6CMnqtZsd3H2xVf5ZDj62dRuzjo2ZTEozbE6u6sy7V4BVGVzTLxZh7fAwvKYhTYSnNG00D9gRoAXe'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': int(total * 100),
                        'product_data': {
                            'name': 'Your Products Cost',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + f'/checkout/payment_successful_stripe/?token={token}',
            cancel_url=YOUR_DOMAIN + f'/checkout/payment_canceled/?token={token}',
            client_reference_id=str(request.user.id),
            customer_email=request.user.email,
            metadata={'token': token}
        )

        address = Address.objects.get(customer=request.user, default=True)

        if not Order.objects.filter(order_key=checkout_session.id).exists():
            order = Order.objects.create(
                user_id=request.user.id,
                email=request.user.email,
                full_name=address.full_name,
                address1=address.address_line,
                address2=address.address_line2,
                city=address.town_city,
                phone=address.phone,
                postal_code=address.postcode,
                total_paid=total,
                order_key=token,
                payment_option="stripe",
            )
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"]
                )

    except Exception as e:
        return str(e)

    return HttpResponseRedirect(checkout_session.url)


def payment_canceled(request):
    user_email = request.user.email
    current_url = request.build_absolute_uri()
    parsed_url = urlparse(current_url)
    query_params = parse_qs(parsed_url.query)
    if 'token' in query_params:
        token_value = query_params['token'][0]
    try:
        order = Order.objects.get(email=user_email, order_key=token_value, billing_status=False)
        order.delete()
    except Order.DoesNotExist:
        pass
    return render(request, 'checkout/payment_canceled.html')

