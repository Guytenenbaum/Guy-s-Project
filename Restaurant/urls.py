from django.urls import path
from . import views 


urlpatterns= [
    path('',views.main, name = 'main-page'),
    path('about/',views.about, name='about'),
    path('reviews/',views.reviews, name='reviews')
]