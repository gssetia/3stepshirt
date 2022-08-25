"""
Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Item, Order
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def about(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request, 'about.html', context)

@login_required
def cart(request):

    try:
        order = Order.objects.get(user = request.user)
        
        if request.method == "POST":

            item_to_delete = order.items.get(title = request.POST['item'])
            
            order.items.remove(item_to_delete)
            item_to_delete.delete()

        context = {
            'order':order,
        }
    
        return render(request, 'cart.html', context)

    except ObjectDoesNotExist:
        messages.error(request, "You do not have anything in your cart")
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
                    print(item, type(item))
                    order.items.add(item)
            order.save()

            return redirect("/design")

    else:
        form = ItemForm()
    
    return render(request, 'design.html', {"form":form})

def home(request):
    context = {
        'items':Item.objects.filter(user=request.user),
        'order':Order.objects.filter(user=request.user),
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