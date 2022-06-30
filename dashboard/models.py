from email import message
from typing_extensions import Self
from click import password_option
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    
    user_name = models.CharField(max_length=30, blank=True)
    user_email = models.CharField(max_length=30, blank=True)
    sujet = models.CharField(max_length=30, blank=True)
    message = models.CharField(max_length=100, blank=True)
   
class Admin(models.Model):
    id_admin = models.CharField(max_length=30, blank=True)
    login = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=30, blank=True)
    

class Order(models.Model):
    product_category = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    shipping_cost = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

class Recherche(models.Model):
    url = models.URLField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)

class Download(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=50)
    