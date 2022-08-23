"""
Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Item, Order
from .forms import ItemForm

def about(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request, 'about.html', context)

def cart(request):
    print(request.method)
    if request.method == "POST":
        
        
        order_list = Order.objects.filter(user=request.user, ordered=False)
        if order_list.exists():
            order = order_list[0]
            
        else:
            print("um")
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            
        for item in Item.objects.all():
                order.items.add(item)
        order.save()

        return redirect("/")

    else:
        context = {
            'items':Item.objects.all(),
        }
    
    return render(request, 'cart.html', context)

def design(request):
    
    if request.method == "POST":
        form = ItemForm(request.POST)
        print(form.data)
 
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect("/design")
        
        print(form.errors)

    else:
        form = ItemForm()
    
    return render(request, 'design.html', {"form":form})

def home(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request, 'home-page.html', context)


def add_to_cart(request):
    item = get_object_or_404(Item)
    print(item)
    
    order_list = Order.objects.filter(user=request.user, ordered=False)
    if order_list.exists():
        order = order_list[0]
        order.items.add(item)
        
    else:
        print("um")
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(item)

    order.save()

    return redirect("/")