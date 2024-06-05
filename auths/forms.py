from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from catalog.excel import Excel

def phone_validator(value):
    if not value.isdigit:
        raise ValidationError("phone number must be a number")
    else:
        pass

def username_validator(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError("username already exists")
    else:
        pass

class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'md-form-control', 'placeholder': 'username', "id":"InputUsername"}), validators=[username_validator])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'md-form-control', 'placeholder': 'email', "id": "InputEmail"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'md-form-control', 'placeholder': 'Phone Number', "id": "InputPhone"}), validators=[phone_validator])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'md-form-control', 'placeholder': 'Password', 'id':"InputPassword"}))                                
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'md-form-control', 'placeholder': 'Confirm Password', 'id':"InputPasswordConfirm"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', "password2", "main_stack"]
        

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), validators=[phone_validator])
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', "cols": 60, "rows": 5}))
    main_stack = forms.ChoiceField(choices=Excel.stack_icon, widget=forms.Select(attrs={"class": "form-control"}))
    # images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': ''}))
                                                     
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "main_stack", "images", "phone_number", "bio"]
  
class StackForm(forms.ModelForm):
    stack = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'stack' }))
    rating = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'rating' }))
    hobbies = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'hobbies',}))
    
    class Meta:
        model = Skill
        fields = "__all__"
        exclude = ['user']
              
StackBlockset = inlineformset_factory(User, Skill, extra=2, can_delete=False, form=StackForm, max_num=2)
        
class RoomForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room', 'id': "room_name", "name": "room_name"}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':  'Enter Description', 'id': "description_room", "name": "description_room"}), required=True)
    
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'topic', 'participant']
        

class UserForm2(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), validators=[phone_validator])
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        
class CustomerForm(forms.ModelForm):
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    town = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Town'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}))
    order_note = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Order Note on special orders'}))
    class Meta:
        model = Customer
        exclude = ['user']
        fields = ["country", "state", "address", "town", "postal_code", "order_note"]