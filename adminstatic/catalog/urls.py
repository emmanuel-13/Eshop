from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('shop/<slug>/', shop_details, name='shop_details'),
    path('product_review/', product_review, name='product_review'),
    path('checkout/', checkout, name='checkout'),
    path('verify_payment/<str:ref>', verify_payment, name='verify_payment'),
    path('success/', success, name='success'),
    path("cart_view/", cart_view, name='cart_view'),
    path("add/<int:pk>/", cart_add, name='cart_add'),
    path("delete/<int:id>/", cart_delete, name='cart_delete'),
    path("update/<int:id>/", cart_update, name='cart_update'),
]