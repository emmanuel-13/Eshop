from django import template
from catalog.models import *
from django.db.models import Q
from django.contrib import messages

register = template.Library()

@register.inclusion_tag("components/category.html")
def category(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # messages.info(request, f"{q} found but not functioning now")
    variant = request.GET.get('variant') if request.GET.get('variant') != None else ''
    if q:
        category = Category.objects.filter(Q(name__icontains=q))
        if category:
            pass
        else:
            category = Category.objects.all().order_by("date_created")[:10]
        return {"category": category}
    
    elif variant:
        category = Category.objects.filter(Q(name=variant))
        if category:
            pass
        else:
            category = Category.objects.all().order_by("date_created")[:10]
        return {"category": category}
    else:
        category = Category.objects.all().order_by("date_created")[:10]
        return {"category": category}
    
@register.simple_tag
def get_total_price(user):
    try:
        cart = Cart.objects.get(user=user, is_paid=False)
        my_cart = cart.get_cart_total()
    except Exception as e:
        my_cart = 0
    return my_cart

@register.simple_tag
def get_item_count(user):
    cartitems = CartProduct.objects.filter(cart__is_paid=False, cart__user=user).count()
    return cartitems