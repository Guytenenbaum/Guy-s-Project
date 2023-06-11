from django.db import models
from django.contrib.auth.models import User 
from Restaurant.models import Dish   
#user

class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE) 
    
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'cart'

class Delivery(models.Model):
    order_id = models.OneToOneField(Cart,on_delete=models.CASCADE,primary_key=True)
    is_delivered = models.BooleanField(default=False)
    address = models.CharField(max_length=100,blank=False)
    comment = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    total_price=models.IntegerField(default=0, blank=False)
    
    class Meta:
        db_table = 'delivery'
    
    
class Item(models.Model):
    dish_id= models.ForeignKey(Dish,on_delete=models.CASCADE)
    cart_id= models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount=models.IntegerField(blank=False)
    
    class Meta:
        db_table = 'item'
    def __str__(self):
        return str(self.id)
