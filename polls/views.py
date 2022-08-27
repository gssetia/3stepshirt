"""
Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Item, Order, BillingAddress, Payment
from .forms import ItemForm, CheckoutForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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
            order = Order.objects.get(user = request.user)
            if form.is_valid():
                obj = form.cleaned_data
                payment_option = obj.get('payment_option')
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
    return render(request, 'checkout.html', {"form":form})


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

        order = Order.objects.get(user = request.user)
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
        messages.info(request, "You do not have anything in your cart.")
        messages.error(request, "You do not have anything in your cart.")
        return redirect("/")

    
@login_required
def design(request):

    if request.method == "POST":
        form = ItemForm(request.POST)
        print(form.data)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.price = 100
            obj.user = request.user
            obj.save()

            order_list = Order.objects.filter(user=request.user, ordered=False)
            if order_list.exists():
                order = order_list[0]
            
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=request.user, ordered_date=ordered_date)
                    
            item_list = Item.objects.filter(user=request.user)
            for item in item_list:
                if item not in order.items.all():
                    #print(item, type(item))
                    messages.info(request, "This item was added to your cart.")
                    order.items.add(item)
                    order.quantity += item.quantity
            order.save()

            return redirect("/design")

    else:
        form = ItemForm()
    
    return render(request, 'design.html', {"form":form})

def home(request):
    context = {
        'items':Item.objects.all(),
    }
    return render(request, 'home-page.html', context)

@login_required
def remove_from_cart(request):  
    print(request.GET.get)
    #<a href="{{ object.get_remove_from_cart_url }}" class="btn btn-primary btn-md my-6 p"> remove from Cart</a>

    return redirect("/cart")
    #return redirect("../")

def get_remove_from_cart_url(request):
    print("test")
    return reverse("add-to-cart", kwargs={
        'value':self.title
    })