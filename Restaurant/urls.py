from django.urls import path
from . import views 


urlpatterns= [
    path('main/',views.main, name = 'main-page'),
    path('about/',views.about, name='about'),
    path('reviews/',views.reviews, name='reviews')
]