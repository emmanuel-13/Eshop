from django import template
from auths.models import *
import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from catalog.models import *

register = template.Library()

@register.inclusion_tag("dashboard/inclusion/user_notification.html")
def mess_notification(user):
    mess_list = []
    room = Room.objects.all()
    for room in room:
        if user in room.participant.all():
            message = Message.objects.filter(room=room, date_updated__date=timezone.now().date())[:3]
            for message in message:
                if user != message.user:
                    mess_list.append(message)
                else:
                    pass
            break
        else:
            pass
    # print(mess_list)
    message = mess_list
    return {"message": message}

@register.simple_tag
def total_messages(user):
    mess_list = []
    room = Room.objects.all()
    for room in room:
        if user in room.participant.all():
            message = Message.objects.filter(room=room, date_created__date=timezone.now().date())[:3]
            print(message)
            for message in message:
                print(message.user)
                if user != message.user:
                    mess_list.append(message)
                else:
                    pass
            break
        else:
            pass
    print(len(mess_list))
    total = len(mess_list)
    return total

@register.inclusion_tag("dashboard/inclusion/user_notification.html")
def users_updated():
    user = User.objects.filter(date_joined__date=timezone.now().date()).exists()
    if user:
        start_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = timezone.now()
        user_joined = User.objects.filter(date_joined__range=(start_time, end_time))
        # user_joined.first().date_joined
        time = timezone.now()- user_joined.first().date_joined
        time_to_sec = time.total_seconds()
        hours = int(time_to_sec // 3600)
        mins = int((time_to_sec % 3600) // 60)
        print(mins)
        print(hours)
        if mins <= 0 and hours != 0:
            return {"users": user, "times": f"{hours} hours ago", "info": "new users update"}
        else:
            return {"users": user, "times": f"{mins} minutes ago", "info": "new users update"}
    else:
        user = False
    return {'users': user}
    
@register.inclusion_tag("dashboard/inclusion/user_notification.html")
def profile_updated(user):
    profile = User.objects.get(username=user.username)
    if timezone.now().date() == profile.date_updated.date():
        times = True
        print(timezone.now() - profile.date_updated)
        time = timezone.now()- profile.date_updated
        time_to_sec = time.total_seconds()
        hours = int(time_to_sec // 3600)
        mins = int((time_to_sec % 3600) // 60)
        print(mins)
        print(hours)
        if mins <= 0 and hours != 0:
            return {"times": times,"time": f"{hours} hours ago", 'new': "New profile update"}
        else:
            return {"times": times, "time": f"{mins} minutes ago", 'new': "New profile update"}
    else:
        times = False
        return {'times': times}
    
@register.inclusion_tag("dashboard/inclusion/user_notification.html")
def modal(user):
    mess_list = []
    room = Room.objects.all()
    for room in room:
        if user in room.participant.all():
            message = Message.objects.filter(room=room, date_updated__gte=timezone.now().date())
            for message in message:
                if user != message.user:
                    data = {
                        "name": message.user.username,
                        "body": message.body,
                        "time": message.date_updated
                    }
                    mess_list.append(data)
                else:
                    pass
            break
        else:
            pass
    message = mess_list
    return {"modal": message, "user": user}

@register.filter
def mydate(date_created__date):
    return date_created__date == timezone.now().date()

@register.simple_tag
def paid_purchase(user):
    paid = Purchase.objects.filter(cart__cart__user=user, cart__cart__is_paid=True).count()
    recent_paid = Purchase.objects.filter(cart__cart__user=user, cart__cart__is_paid=True, date_created__gte=timezone.now().date()).count()
    checker = None
    if recent_paid > 1:
        checker = recent_paid
    else:
        checker = paid
    return checker

@register.simple_tag
def pending_purchase(user):
    paid = CartProduct.objects.filter(cart__user=user, cart__is_paid=False).count()
    recent_paid = CartProduct.objects.filter(cart__user=user, cart__is_paid=False).count()
    checker = None
    if recent_paid > 1:
        checker = recent_paid
    else:
        checker = paid
    return checker

@register.simple_tag
def annoucement(user):
    purchase = Purchase.objects.filter(status="deliver").count()
    pending = Purchase.objects.filter(status="pending").count()
    messages = Message.objects.filter(room__participant=user).count()
    total = purchase + pending + messages
    return total

from django.utils.html import format_html

@register.simple_tag
def check_purchase(user):
    paid = Purchase.objects.filter(cart__cart__user=user, cart__cart__is_paid=True, date_created__gte=timezone.now().date()).exists()
    cart = CartProduct.objects.filter(cart__user=user, cart__is_paid=False).exists()
    if paid:
        new = "New"
        return format_html(
            '<span class="label label-success menu-caption">New</span>',
            new
        )
    elif cart:
        new = "New"
        return format_html(
            '<span class="label label-success menu-caption">New</span>',
            new
        )
    return ""

@register.simple_tag
def check_paid_purchase(user):
    paid = Purchase.objects.filter(cart__cart__user=user, cart__cart__is_paid=True, date_created__gte=timezone.now().date()).exists()
    # print(pending)
    if paid:
        new = "New"
        return format_html(
            '<span class="label label-success menu-caption">{}</span>',
            new
        )
    else:
        return ""
    
@register.simple_tag
def check_pending_purchase(user):
    pending = CartProduct.objects.filter(cart__user=user, cart__is_paid=False, date_created__gte=timezone.now().date()).exists()
    # print(pending)
    if pending:
        new = "New"
        return format_html(
            '<span class="label label-success menu-caption">{}</span>',
            new
        )
    else:
        return ''