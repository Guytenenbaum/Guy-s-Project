from django.urls import path
from . import views 


urlpatterns= [
        path('editcategories/',views.edit_categories, name='edit-categories'),
        path('editdishes/',views.edit_dishes, name='edit-dishes'),
        path('managerlogin/',views.manager_login, name='manager-login'),
        path('allorders/',views.all_orders, name='all-orders'),
]