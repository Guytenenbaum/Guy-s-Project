from django.contrib import admin
from django.urls import path, include

 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Clients.urls")),
    path('',include("Restaurant.urls")),
    path('',include("Managers.urls") )
]
