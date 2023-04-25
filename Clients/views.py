from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from Restaurant.models import *
from .models import *
from django.utils import timezone 
# Create your views here.

@login_required(login_url="login")
def menu(request):
    current_user=request.user
    my_cart=Cart.objects.filter(user_id=current_user.id).latest('id')
    dishes=Dish.objects.all()
    categories=Category.objects.all()
    context={"dishes":dishes,
             "categories":categories,}
    if request.method=='POST':
        dish_id=request.POST['dish_id']
        quantity=request.POST['quantity']
        dish=Dish.objects.get(id=dish_id)
        if Item.objects.filter(cart_id=my_cart,dish_id=dish.id):
            item=Item.objects.get(cart_id=my_cart,dish_id=dish.id)
            item.amount+=int(quantity)
            item.save()
        else:
            new_item= Item(
                dish_id=dish,
                cart_id=my_cart,
                amount=quantity    
                )
            new_item.save()
    return render(request, "menu.html",context=context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/menu')
    if request.method == "POST":
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password']
                            )
        if user is not None:
            login(request,user)
            return render(request,'main.html')
        else:
            context={'failed':True}
            return render(request,'login.html',context=context)
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return render(request,'main.html')


def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email=request.POST['email']
        if form.is_valid():
            user= form.save()
            user.email=email 
            user.save()
            new_cart=Cart(user=user)
            new_cart.save()
            return render(request,'login.html')
    return render(request,'signup.html',{"form":form})

class CartItem():
    def __init__(self,dish ,amount):
        self.dish=dish
        self.amount=amount
        self.price=dish.price*amount
def total_price(request):
    current_user = request.user
    my_cart = Cart.objects.filter(user_id=current_user.id).latest('id')
    items = Item.objects.filter(cart_id=my_cart.id)
    cart_items=[CartItem(Dish.objects.get(id=item.dish_id.id),item.amount) for item in items ]
    sum=0
    for item in cart_items:
        sum+=item.price
    return my_cart,cart_items,sum

@login_required(login_url="login")    
def show_cart(request):
    current_user=request.user
    my_cart, cart_items, sum = total_price(request)
    if len(cart_items)==0:
        return menu(request)
    if request.method=='POST':
        new_amount=request.POST['amount']  
        dish_id=request.POST['dish']
        item=Item.objects.get(cart_id=my_cart,dish_id=dish_id)
        if int(new_amount)==0:
            item.delete()
        else:
            item.amount=int(new_amount)
            item.save()
        return redirect(request.path)
    return render(request, 'show_cart.html', {"cart_items": cart_items,"sum":sum})


@login_required(login_url="login")
def order(request):
    current_user=request.user
    my_cart, cart_items, sum = total_price(request)
    if request.method == "POST":
        order_id=my_cart
        new_delivery=Delivery(
            order_id=order_id,
            is_delivered=False,
            address=request.POST['full_address'],
            comment=request.POST['special_requests'],
            created=timezone.now(),
            total_price=sum
        )
        new_delivery.save()
        new_cart=Cart(user=current_user)
        new_cart.save()
        return render(request,'order_summary.html',{"new_delivery":new_delivery})
    return render(request, 'order.html')

@login_required(login_url="login")
def order_summary(request):
    current_user = request.user
    my_cart = Cart.objects.filter(user_id=current_user.id).latest('id')
    items = Item.objects.filter(cart_id=my_cart.id)
    cart_items=[CartItem(Dish.objects.get(id=item.dish_id.id),item.amount) for item in items ]
    sum=0
    for item in cart_items:
        sum+=item.price
    if request.method=='POST':
        order_id=request.POST['delivery_id']
        if Delivery.objects.get(order_id=order_id).is_delivered:
            return HttpResponse("can't change information because the shipment is already on its way.")
        else:
            return render(request,'update_details.html',{"order_id":order_id})
    return render(request, 'order_summary.html')

@login_required(login_url="login")
def all_orders(request):
    order_history=[]
    current_user = request.user
    client_cart=Cart.objects.filter(user=current_user)
    for cart in client_cart:
        delivery=Delivery.objects.filter(order_id=cart)
        if delivery.exists():
            order_history.append(delivery[0])
    return order_history

@login_required(login_url="login")
def order_history(request):
    order_history = all_orders(request)
    if request.method=='POST':
        order_id=request.POST['order_id']
        if Delivery.objects.get(order_id=order_id).is_delivered:
            return HttpResponse("Can't change information because the shipment is already on its way.")
        else:
            return render(request,'update_details.html',{"order_id":order_id})
    return render(request,'order_history.html',{"order_history":order_history})

@login_required(login_url="login")
def update_details(request):
    if request.method == "POST":
        order_id=request.POST['order_id']
        new_delivery=Delivery.objects.get(order_id=order_id)
        new_delivery.address=request.POST['full_address']
        new_delivery.comment=request.POST['special_requests']
        new_delivery.save(update_fields=['address','comment'])
        return render(request,'order_summary.html',{"new_delivery":new_delivery})
    return render(request,'update_details.html')

@login_required(login_url="login")
def update_user(request):
    current_user = request.user
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email = request.POST.get('email') 
        if form.is_valid():
            if current_user.username != form.cleaned_data['username'] and User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, 'update_user.html', {"form": form, "username_is_taken": True})
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                return render(request, 'update_user.html', {"form": form, "not_valid_password": True})
            current_user.username = form.cleaned_data['username']
            current_user.set_password(form.cleaned_data['password1'])  
            current_user.email = email
            current_user.save(update_fields=['username', 'email'])  
            return render(request, 'main.html')
    return render(request, 'update_user.html', {"form": form})