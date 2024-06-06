from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from .models import *
from .forms import *
from django.contrib import messages
from django.views.generic import *
from django.utils import timezone
from catalog.models import *

@login_required(login_url="login")
def paid(request):
    paids = True
    paid = Purchase.objects.filter(cart__cart__user=request.user, cart__cart__is_paid=True).order_by("-date_updated")
    return render(request, "dashboard/paid_pending.html", {'paid': paid, 'paids': paids})


@login_required(login_url="login")
def pending(request):
    pend = True
    pending = CartProduct.objects.filter(cart__user=request.user, cart__is_paid=False).order_by("-date_created")
    return render(request, "dashboard/paid_pending.html", {'pend': pend, "pending": pending})


@login_required(login_url='login')
def dashboard(request):
    purchase = Purchase.objects.filter(cart__cart__user=request.user, cart__cart__is_paid=True).count()
    purchase_arrive = Purchase.objects.filter(cart__cart__user=request.user, cart__cart__is_paid=True, date_created__gte=timezone.now().date()).count()
    dashboard = True
    mymesssage = []
    room = Room.objects.filter(participant=request.user).count()
    
    if room > 0:
        mes = Room.objects.filter(participant=request.user).order_by('-date_updated').first().message_set.first()
    else:
        mes = ""
    # print(messages.room.name)
    
    todo = Todo.objects.filter(user=request.user).order_by("-date_updated")[:4]
    messages = Message.objects.filter(date_updated__gte=timezone.now().date()).order_by("-date_updated")
    room = Room.objects.all().order_by("-date_updated")
    cart_items = CartProduct.objects.filter(cart__user=request.user, cart__is_paid=True).count()
    cart_checker = CartProduct.objects.filter(cart__user=request.user, cart__is_paid=False).count()
    
    for message in messages:
        if request.user in message.room.participant.all():
            # print(message.user, message.room)
            data = {
                "username": message.user.username,
                "body": message.body,
                "room": message.room.participant.all()
            }
            mymesssage.append(data)
        else:
            pass
    user = User.objects.all().order_by("-date_updated")[:6]
    products = list(Product.objects.values('price', 'name').order_by('-date_created'))[:4]
    
    # print(mymesssage)
    return render(request, 'dashboard/index1.html', {'dashboard': dashboard, "todo": todo, 'purchase_arrive': purchase_arrive,
                                                     "message": mymesssage, "room": room, 'user': user, 'mes': mes, 'pro': products,
                                                     'product': cart_items, 'purchase': purchase, "room": room, "cart": cart_checker})

def delete_todo(request, pk):
    todo = Todo.objects.get(user=request.user, pk=pk)
    todo.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))

def mylogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    msg = None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except:
            msg = "Email doesn\'t exist"
            messages.info(request, msg)
            return redirect("login")
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            print(user.username)
            login(request, user)
            messages.success(request, "login successfully")
            return redirect('home')
        else:
            print("user does not exists")
            if not User.objects.filter(password=password).exists():
                messages.warning(request, "incorrect password")
            else:
                messages.info(request, "account doesn\'t exists")
            return redirect('login')
    return render(request, 'dashboard/login1.html')

@csrf_exempt
def username_validation(request):
    data = json.loads(request.body)
    username = data['username']
    
    if not str(username).isalnum():
        return JsonResponse({"error": f"Username {username} is alphanumeric"})
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': f"Username {username} already exists"})
    
    return JsonResponse({'success': f'Username {username} is valid'})

@csrf_exempt
def email_validate(request):
    data = json.loads(request.body)
    email = data['email']
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': f'Email {email} already exists'})
    return JsonResponse({'success': f"Email {email} is valid"})

@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        messages.error(request, "error processing data")
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "login successfully")
            return redirect('dashboard')
        else:
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                messages.info(request, f" {form.cleaned_data.get('username')} already exists")
                return redirect('register')
            elif User.objects.filter(email=form.cleaned_data.get('email')).exists():
                messages.info(request, f"{form.cleaned_data.get('email')} already exists")
                return redirect('register')
            else:
                messages.info(request, 'invalid details passed')
                return redirect('register')
    
    form = UserForm()
    
    return render(request, 'dashboard/register1.html', {'form': form})

def mylogout(request):
    logout(request)
    messages.info(request, "logout successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="login")
def profile(request):
    template_name = "dashboard/profile1.html"
    user = User.objects.get(username=request.user.username)
    skill = Skill.objects.filter(user=request.user)
    profile = True
    form = ProfileForm(instance=request.user)
    skill_form = StackBlockset(instance=request.user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        skill_form = StackBlockset(request.POST, request.FILES, instance=request.user)
        print(skill_form.instance)
        if form.is_valid() and skill_form.is_valid():
            user = form.save()
            skill_form = skill_form.save(commit=False)
            
            for skills in skill_form:
                skills.user = user
                skills.save()
                
            messages.success(request, f"{form.cleaned_data['username']} save successfully")
            return redirect('profile')
        else:
            messages.info(request, "Error saving profile")
            return redirect('profile')
    
    context = {'profile': profile,"skills": skill, 'form': form, 'formset': skill_form}
    
    return render(request, template_name, context)
 
@login_required(login_url="login")   
def setting(request):
    product = Product.objects.filter(date_created__gte=timezone.now().date())
    total = Product.objects.all()
    view = RecentView.objects.filter(user=request.user)
    recent = Message.objects.filter(room__participant=request.user, date_updated__gte=timezone.now().date())
    room = Room.objects.filter(participant=request.user)
    pro = Product.objects.all().order_by('date_created')[:10]
    print(pro)
    return render(request, 'dashboard/settings.html', {"settings": True, 'pro': product, 'total': total, 'product': pro,
                                                       "view": view, 'message': recent, 'room': room})

def todo(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.user
        if Todo.objects.filter(name=name).exists():
            return JsonResponse({"info": f"{name} already exists"})
        else:
            Todo.objects.create(user=username, name=name)
            return JsonResponse({"success": True})
    return JsonResponse({"error": False})
  
from django.core.paginator import Paginator
  
@login_required(login_url="login")              
def annoucement(request):
    purchase = Purchase.objects.filter(status="deliver")
    paginator = Paginator(purchase, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    pending = Purchase.objects.filter(status="pending").order_by("-date_created")[:5]
    # room = Room.objects.filter(participant=request.user)
    messages = Message.objects.all()
    return render(request, 'dashboard/annoucement.html', {'annoucement': True, "pur": page_obj,
                                                          "pending": pending, 'mess': messages})
    

@login_required(login_url="login")
def community(request):
    topic = Topic.objects.all().order_by("-date_updated")[:4]
    room = Room.objects.all().order_by("-date_updated")[:4]
    messages = Message.objects.filter(date_updated__gte=timezone.now().date()).order_by("-date_updated")[:4]
    rooms_form = RoomForm()
    
    follows = []
    discover = []
    new = []
    following = Room.objects.all().order_by("-date_updated")
    for following in following:
        if request.user in following.participant.all():
            follows.append(request.user)
            
            for mess in following.message_set.all():
                new.append(mess.room)
        else:
            discover.append(request.user)
    
    myfollow = len(follows)
    mydiscover = len(discover)
    if new == []:
        new.append("No Room Engaged")
    return render(request, 'dashboard/community.html', {'community': True, 'room': room, "topic": topic,"pop": new[0],
                                                        "myfollow" : myfollow, "mydiscover": mydiscover,
                                                        'rooms_form': rooms_form, "messages": messages})

@login_required(login_url="login")
def join(request):
    if request.method == 'POST':
        id = request.POST.get("id", None)
        room = Room.objects.get(id=id)
        room.participant.add(request.user)
        msg = f"You have successfully joined {room}"
        return JsonResponse({'status': True, "msg": msg})
    
@login_required(login_url="login")
def leave(request):
    if request.method == 'POST':
        id = request.POST.get("id", None)
        room = Room.objects.get(id=id)
        room.participant.remove(request.user)
        msg = f"Hello {request.user.username}, You have successfully left the rooms {room}"
        return JsonResponse({'status': True, "msg": msg})

@login_required(login_url="login")
def mytopic(request):
    topic = list(Topic.objects.values())
    print(topic)
    return JsonResponse(topic, safe=False)

@login_required(login_url='login')
def room(request, name):
    try:
        room = Room.objects.get(name=name)
        form = RoomForm(instance=room)
        participant = room.participant.all()
        topic = Topic.objects.all().order_by("-date_updated")
        room_message = room.message_set.all().order_by("-date_created")
    except Room.DoesNotExist:
        return redirect("community")
    return render(request, 'dashboard/room.html', {"room": room, 'participant': participant, 
                                                   'form': form, "topic": topic, "room_message": room_message})

def create_message(request):
    if request.method == "POST":
        id = request.POST.get("id", None)
        message = request.POST.get("message", None)
        room = Room.objects.get(id=id)
        Message.objects.create(
            room=room, user=request.user, body=message
        )
        return JsonResponse({"status": True})
    
def clear(request):
    status = request.POST.get("status", None)
    return JsonResponse({"status": True})

def delete_messages(request):
    if request.method == "POST":
        id = request.POST.get("id", None)
        message = Message.objects.get(id=id)
        message.delete()
        data = {
            "deleted": True
        }
        return JsonResponse(data, safe=False)
    
def update_message(request):
    if request.method == "POST":
        id = request.POST.get("id", None)
        mes = request.POST.get("mes", None)
        
        obj = Message.objects.get(id=id)
        obj.body = mes
        obj.save()
        
        user = {
            "id": obj.id, "body": obj.body, "room": obj.room, "user": request.user
        }
        
        data = {
            "user": user
        }
        
        return JsonResponse(data)
    
@login_required(login_url="login")
def room_form(request):
    topic = Topic.objects.all()
        
    if request.method == "POST":
        topic = request.POST.get('topic', None)
        topic, create = Topic.objects.get_or_create(name=topic)
        room = Room.objects.create(
            topic=topic, host=request.user, name=request.POST.get("room", None),
            description=request.POST.get("description", None)
        )
        room.participant.add(request.user)
        msg = "Room Created successfully"
        return JsonResponse({"status": True, "link": "community", "msg": msg})
    else:
        msg = "Room not created"
        return JsonResponse({"status": False, "link": "community", 'msg': msg })
        
@login_required(login_url='login')
def room_update(request):
    topic = Topic.objects.all()
    
    if request.method == 'POST':
        id = request.POST.get("id", None)
        print(id)
        room = Room.objects.get(pk=id)
        print(room)
        topic = request.POST.get("topic", None)
        topics, created = Topic.objects.get_or_create(name=topic)
        room.name = request.POST.get("room", None)
        room.topic = topics
        room.description = request.POST.get("description", None)
        room.save()
        
        msg = f"{room.name} updated successfully"
        return JsonResponse({"status": True, "msg": msg, "link": "community"})
        
@login_required(login_url="login")
def room_delete(request):
    if request.method == "POST":
        data = request.POST.get("id", None)
        room = Room.objects.get(pk=data)
        room.delete()
        msg = f"Room {data} Deleted successfully"
        return JsonResponse({"status": True, 'msg': msg})
    


    