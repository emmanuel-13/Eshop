import secrets
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from PIL import Image
from django.urls import reverse
from catalog.excel import Excel
from catalog.paystack import Paystack

def only_number(value):
    if not value.isdigit():
        if len(value) == 11:
            pass
        raise ValidationError("Only numbers are allowed")
    else:
        pass


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    images = models.ImageField(upload_to="profile/", blank=True, null=True, default='../static/img/user.jpg')
    phone_number = models.CharField(max_length=11, validators=[only_number])
    date_updated = models.DateTimeField(auto_now=True)
    main_stack = models.CharField(max_length=50, choices=Excel.stack_icon, default=Excel.stack_icon[0])
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # if self.images:
        #     img = Image.open(self.images.path)
            
        #     if img.height >= 250 and img.width >= 250:
        #         output_size = (250, 250)
        #         img.thumbnail(output_size)
        #         img.save(self.images.path)
        # else:
        #     pass
        
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stack = models.CharField(max_length=255, null=True, blank=True, default="")
    rating = models.IntegerField(default=0, null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    icons = models.ImageField(upload_to="icons", blank=True, null=True, default="../static/images/gallery/cd-icon-navigation.svg")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_created', '-date_updated']
        
    def __str__(self):
        return self.stack
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.icons.path)
        
        if img.height >= 250 and img.width <= 450:
            output = (250, 450)
            img.thumbnail(output)
            img.save(self.icons.path, quality=50)
        else:
            pass


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="topic")
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"
        ordering = ['date_created', 'date_updated']
    
    
class Topic(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date_created', 'date_updated']
        
        
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="host")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    participant = models.ManyToManyField(User, blank=True, related_name="participant")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date_created', 'date_updated']
    
        
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def room_host(self):
        return self.room.host.username

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-date_created', '-date_updated']
        
    def get_absolute_url(self):
        return reverse("room", kwargs={"name": self.room.name})

def is_digit(value):
    if not value.isdigit():
        raise ValidationError("postal code must be a number")
    else:
        pass

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=200,  null=True, blank=True)
    address = models.CharField(max_length=200,  null=True, blank=True)
    apartment = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=150, null=True, blank=True)
    postal_code = models.CharField(max_length=6, null=False, blank=False, default=0, validators=[is_digit])
    order_note = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    
        
