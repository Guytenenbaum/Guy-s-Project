from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name= models.CharField(max_length=100,blank=False)
    image= models.CharField(max_length=300,blank=False)
    
    class Meta:
        db_table = 'category'
    def __str__(self):
        return self.name
    
class Dish(models.Model):
    name = models.CharField(max_length=100,blank=False)
    price = models.IntegerField(blank=False,validators=[MinValueValidator(1)])
    description=models.CharField(max_length=200, blank=False)
    image= models.CharField(max_length=300,blank=False)
    is_gluten_free=  models.BooleanField(default=False)
    is_vegeterian=  models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'dish'
    def __str__(self):
        return self.name
