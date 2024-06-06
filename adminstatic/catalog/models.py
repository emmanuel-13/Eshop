import json
import secrets
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from auths.models import Customer, User
from django.utils.html import format_html
from django.contrib import admin

from catalog.paystack import Paystack
from .excel import Excel
from PIL import Image
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField
from ckeditor.fields import RichTextField
from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="icons/", default="../static/images/logo-icon.png", null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True, choices=Excel.choices_color, default=Excel.choices_color[0])
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['date_created', 'date_updated']
        
    @admin.display(description="Names")
    def format_color_html(self):
        return format_html(
            '<span style="color: {}">  {} </span>',
            self.color,
            self.name
        )
    
    def save(self, *args, **kwargs):
        self.name.title()
        super().save(*args, **kwargs)
        if self.image == "":
            pass
        else:
            img = Image.open(self.image.path)
            
            if img.height >= 450 and img.width >= 450:
                output = (450,450)
                img.thumbnail(output)
                img.save(self.image.path)       

class SubCat(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)        
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
        
    class Meta:
        verbose_name = "Sub-Category"
        ordering = ['-date_created', '-date_updated']
          
class Brand(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcat = models.ForeignKey(SubCat, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['-date_created', '-date_updated']
        
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcat = models.ForeignKey(SubCat, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(editable=False, default="")
    descriptions = RichTextField()
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='product/', null=False, blank=False, default='../static/img/testimonial-1.jpg')
    discount = models.FloatField(default=0.0)
    top_rated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse("shop_details", kwargs={"slug": self.slug})
    

    
    def __str__(self) -> str:
        return self.slug
        
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['date_created', 'date_updated']
        
    def check_discount(self):
        if self.discount > self.price:
            raise ValueError("price must be greater than discount")
    
    def new_price(self):
        if self.discount:
            new_price = self.price - self.discount
            return new_price
        else:
            return self.price

    def save(self, *args, **kwargs):
        self.new_price()
        self.check_discount()
        self.slug = slugify(self.name)
        # if self.discount > self.price:
        #     raise ValidationError("discount can\'t be greater than price")
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height >= 450 and img.width >= 450:
            output_size = (450, 450)
            img.thumbnail(output_size)
            img.save(self.image.path, quality=50)
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    ref = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_created', "-date_updated"]
        
    def __str__(self):
        return self.user.username
    
    def get_cart_total(self):
        cart_item = self.cartproduct_set.filter(cart__is_paid=False)
        print(cart_item)
        price = []
        
        for items in cart_item:
            price.append(items.get_price_item())
        
        if len(price) == 1:
            print(price)
            return price[0]
        return sum(price)
    
    def get_cart_total_tax(self):
        return round(1.02 * self.get_cart_total(), 2)
    
    def save(self, *args, **kwargs):
        try:
            while not self.ref:
                ref = secrets.token_urlsafe(50)
                similiar_ref = Cart.objects.filter(ref=ref)
                
                if not similiar_ref:
                    self.ref = ref
            
            super().save(*args, **kwargs)
        except Exception as e:
            print(e)
            
    def amount_value(self) -> int:
        return self.get_cart_total_tax() * 100
            
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref)
        
        if status:
            print(result['amount'])
            return True
        else:
            print(result)
            return False
    
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        ordering = ['-date_created', "-date_updated"]
        
    def get_price_item(self):
        if self.product.discount:
            price = self.quantity * (self.product.price - self.product.discount)
            print(price)
        else:
            price = self.quantity * self.product.price
        return price
    
    def get_cart_status(self):
        if self.cart.is_paid == True:
            return "Paid"
        else:
            return "Pending"

options = (
    ("pending", 'pending'), ('deliver', "deliver")
)

class Purchase(models.Model):
    cart = models.ForeignKey(CartProduct, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, default=options[0][0], choices=options)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.status
    
    def check_new(self):
        if self.date_created.date() == timezone.now().date():
            return format_html(
                "<span class='label label-success'> {} </span>", "new"
            )
        return ''

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Reviews"
        ordering = ["-date_created", "-date_updated"]

class RecentView(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    status = models.BooleanField(default=True)
    date_view = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_updated']
    
    def __str__(self):
        return self.user.username