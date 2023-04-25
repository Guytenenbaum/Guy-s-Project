from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import user_passes_test
from Restaurant.models import  Category
from Clients.views import *    
from django.contrib import messages
from django.urls import reverse

def manager_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/menu')
    if request.method == "POST":
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'],
                            )
        if user is not None and user.is_staff:
            login(request,user)
            return render(request.path)
        else:
            failed=True
            return render(request,'manager_login.html',{"failed":failed})
    return render(request,"manager_login.html")

@user_passes_test(lambda u: u.is_superuser)
def edit_categories(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            name = request.POST.get('name')
            image = request.POST.get('image')
            category = Category(name=name, image=image)
            category.save()
        elif 'edit' in request.POST:
            category_name = request.POST.get('edit')
            category = Category.objects.get(name=category_name)
            new_name = request.POST.get('new_name')
            new_image = request.POST.get('new_image')
            category.name = new_name
            category.image = new_image
            category.save()
        elif 'delete' in request.POST:
            print("delete")
            category_name = request.POST.get('delete')
            category = Category.objects.get(name=category_name)
            category.delete()
    categories = Category.objects.all()
    return render(request, 'edit_categories.html', {'categories': categories})



@user_passes_test(lambda u: u.is_superuser)
def edit_dishes(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            image = request.POST.get('image')
            is_gluten_free = request.POST.get('is_gluten_free',False)
            is_vegeterian = request.POST.get('is_vegeterian',False)
            category_name = request.POST.get('category')
            category = Category.objects.get(name=category_name)
            dish = Dish(name=name, price=price, description=description, image=image, is_gluten_free=is_gluten_free, is_vegeterian=is_vegeterian, category=category)
            dish.save()
        elif 'edit' in request.POST:
            print("edit")
            print(request.POST.get('edit'))
            dish_id = request.POST.get('id')
            dish = Dish.objects.get(id=dish_id)
            new_name = request.POST.get('new_name')
            new_price = request.POST.get('new_price')
            new_description = request.POST.get('new_description')
            new_image = request.POST.get('new_image')
            new_gluten = request.POST.get('new_gluten')
            new_vegeterian = request.POST.get('new_vegeterian')
            new_category_name = request.POST.get('new_category')
            new_category = Category.objects.get(name=new_category_name)
            dish.name = new_name
            dish.price = new_price
            dish.description = new_description
            dish.image = new_image
            dish.is_gluten_free = new_gluten
            dish.is_vegeterian = new_vegeterian
            dish.category = new_category
            dish.save()
        elif 'delete' in request.POST:
            dish_name= request.POST.get('delete')
            dish= Dish.objects.get(name=dish_name)
            dish.delete()
        return redirect('edit-dishes')
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    return render(request, "edit_dishes.html", {'dishes': dishes, 'categories': categories})

@user_passes_test(lambda u: u.is_superuser)
def all_orders(request):
    deliveries = Delivery.objects.all()
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        delivery = get_object_or_404(Delivery, order_id_id=order_id)
        delivery.is_delivered =True
        delivery.save(update_fields=["is_delivered"])
        return redirect(request.path)
    return render(request, 'all_orders.html', {'deliveries': deliveries})
