from django.urls import path
from .views import *

urlpatterns = [
    path("", blog, name='blog'),
    path("<slug:slug>/", blog_details, name='blog_details')
]
