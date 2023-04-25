from django.urls import path
from . import views 


urlpatterns= [
    path('login/',views.login_user, name = 'login'),
    path('menu/',views.menu, name= 'menu-page'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout_user,name="logout"),
    path('showcart/',views.show_cart,name="show-cart"),
    path('order/',views.order, name='order'),
    path('ordersummary/',views.order_summary, name='order-summary'),
    path('orderhistory/',views.order_history, name='order-history'),
    path('updatedetails/',views.update_details,name='update-details'),
    path('updateuser/',views.update_user,name='update-user')
    
]
