"""
Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Item, Order, BillingAddress, Payment, Refund
from .forms import ItemForm, CheckoutForm, RefundForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings

import stripe
import random
import string

stripe.api_key = 'sk_test_51LbTxzAWEaHH0GhFqU9gwCoYzbVaCUjDSMXNT4wUCCLD7ooXEEH4WLflukGR6mmdyvKiK9iS76331gUAa9QGo6Sy00YNNvSvxR'

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def about(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request, 'about.html', context)

@login_required
def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        try:
            order = Order.objects.get(user = request.user, ordered=False)
            if form.is_valid():
                obj = form.cleaned_data
                payment_option = obj.get('payment_option')
                prev_ba = BillingAddress.objects.filter(user = request.user)

                if prev_ba:
                    order.billing_address = prev_ba[0]

                if order.billing_address:
                    order.billing_address.street_address = obj.get('street_address')
                    order.billing_address.apartment_address = obj.get('apartment_address')
                    order.billing_address.country = obj.get('country')
                    order.billing_address.zip = obj.get('zip')
                    order.billing_address.save()
                else:

                    billing_address = BillingAddress(
                        user = request.user,
                        street_address = obj.get('street_address'),
                        apartment_address = obj.get('apartment_address'),
                        country = obj.get('country'),
                        zip = obj.get('zip'),
                    )
                    billing_address.save()
                    order.billing_address = billing_address

                order.save()

                if payment_option == 'S':
                    return redirect('../payment/stripe', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('../payment/paypal', payment_option='paypal')
                else:
                    messages.warning(request, "Invalid Payment Option.")
                    return redirect('/checkout')
            else:
                messages.warning(request, "Failed checkout")
        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active order.")
            return redirect("../cart")

    form = CheckoutForm()
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'order':order,
        'items':Item.objects.all(),
        'form':form,
    }
    return render(request, 'checkout.html', context)


def payment(request, payment_option):

    if request.method == "POST":
        
        token = request.POST.get('stripeToken')
        order = Order.objects.get(user=request.user, ordered=False)
        amount=int(order.get_total_price() * 100)

        try:
            # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
                amount=amount, #cents
                currency="cad",
                source=token,
            )
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = request.user
            payment.amount = order.get_total_price()
            payment.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()
            messages.success(request, "Your order was successful.")
            return redirect('/')

        except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect('/')
          
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "Rate Limit Error")
            return redirect('/')
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid Parameters")
            return redirect('/')
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Not Authenticated")
            return redirect('/')
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network Error")
            return redirect('/')
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, "Something went wrong. You were not charged, please try again.")
            return redirect('/')
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            # send email to yourself - code issue.
            messages.error(request, "A serious error occurred. We have been notified.")
            return redirect('/')


    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'order':order,
        'items':Item.objects.all()
    }
    return render(request, 'payment.html', context)

@login_required
def cart(request):
    try:

        order = Order.objects.get(user = request.user, ordered=False)
        context = {
            'order':order,
        }
        if request.method == "POST":

            if 'checkout' in request.POST:
                return redirect("../checkout/")
            
            item_to_delete = order.items.get(title = request.POST['item'])
            messages.info(request, "This item was deleted from your cart.")
            order.items.remove(item_to_delete)
            order.quantity -= item_to_delete.quantity
            order.save()
            item_to_delete.delete()
        
        
    
        return render(request, 'cart.html', context)

    except ObjectDoesNotExist:
        messages.error(request, "You do not have anything in your cart.")
        return redirect("/")

    
@login_required
def design(request):

    if request.method == "POST":
        form = ItemForm(request.POST)
        print(form.data)

        if form.is_valid():
            item = Item()
            obj = form.cleaned_data

            item.title = obj.get('title')
            item.size = obj.get('size')
            item.design = obj.get('design')
            item.quantity = obj.get('quantity')
            item.colour = obj.get('colour')
            item.price = 100
            item.user = request.user
            item.save()

            order_list = Order.objects.filter(user=request.user, ordered=False)
            if order_list.exists():
                order = order_list[0]
            
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                    

            order.items.add(item)
            order.quantity += item.quantity

            messages.info(request, "This item was added to your cart.")
            order.save()

            return redirect("/design")

    else:
        form = ItemForm()

    items = Item.objects.filter(user=request.user)
    context = {
        'items':items,
        'form':form
    }
    return render(request, 'design.html', context)

def home(request):

    return render(request, 'home-page.html')


@login_required
def profile(request):  
    order = Order.objects.filter(user=request.user)
    context = {
        'order':order,
    }
    return render(request, 'profile.html', context)


@login_required
def refund(request):  

    if request.method == "POST":
        form = RefundForm(request.POST)

        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')

            try:
                order = Order.objects.get(ref_code = ref_code)
                
            except ObjectDoesNotExist:
                messages.error(request, "You do not have a valid order.")
                return redirect("/")

            if order.ordered and not order.delivering:

                order.refund = True
                order.save()
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.ref_code = ref_code 
                refund.user = request.user
                refund.save()

            elif order.delivered:
                messages.error(request, "Cancellation error: Your order has already been delivered.")
                return redirect("/")
            else: 
                messages.error(request, "Cancellation error: Your order is already being delivered.")
                return redirect("/")

    order = Order.objects.filter(user=request.user, ordered = False)
    context = {
        'order':order,
    }
    return render(request, 'home-page.html', context)
