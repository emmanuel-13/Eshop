from typing import Any
from django import forms
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.http import HttpRequest
from .models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class SkillInline(admin.StackedInline):
    model = Skill
    extra = 1

class CustomerInline(admin.StackedInline):
    model = Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'state', 'address', 'postal_code', 'order_note']
    list_editable = ['address', 'postal_code', 'order_note']
    search_fields = ['user', 'country', 'state', 'address', 'postal_code']
    list_filter = ['country', 'state', 'address', "date_created", "date_updated"]
    list_display_links = ['country']
    list_per_page = 10
    list_max_show_all = True

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined', 'phone_number', 'date_updated']
    list_editable = ['username']
    list_display_links = ['email']
    list_filter = ['date_joined', "is_staff", "is_superuser", "is_active"]
    search_fields = ['username', 'email', 'phone_number']
    list_per_page = 10
    list_max_show_all = 20
    inlines = [SkillInline, CustomerInline]
    
    def has_add_permission(self, request: HttpRequest):
        if request.user.is_superuser:
            return True
        return False
        # return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):
        if obj is not None and obj == request.user:
            return True  # User can change their own profile  # Others can't change profiles
    
    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj == request.user:
            return True  # User can delete their own profile
        elif request.user.is_superuser:
            return True  # Superuser can delete any profile
        return False 
        
    
    def has_view_permission(self, request: HttpRequest, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['name', 'status']
        exclude = ['user']
    
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    form = TodoForm
    list_display = ['user', 'name', 'status', 'date_created', 'date_updated']
    list_editable = ['status']
    search_fields = ['name', 'status', 'user']
    list_filter = ['date_created', 'date_updated', 'user', 'status']
    fieldset = (
        (
            "User-details", {"fields": ['user', 'name', 'status']}
        ),
        ('Date', {'fields': ["date_created", 'date_updated']})
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        obj.save()
    

class RoomInline(admin.StackedInline):
    model = Room
    extra = 1
    fields = ['name', 'description']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.host == request.user:
            kwargs["queryset"] = kwargs.get("queryset", db_field.remote_field.model.objects).exclude(host=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_created', 'date_updated']
    inlines = [RoomInline]
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Room):
                # Set the user to the current logged-in user
                instance.host = request.user
                instance.save()
        formset.save_m2m()
        super().save_formset(request, form, formset, change)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', "room_host", 'date_created', "date_updated"]
    list_filter = ['user', 'room', 'date_created', "date_updated"]
    search_fields = ['user', 'room']
    list_per_page = 10

class MessageInline(admin.StackedInline):
    model = Message
    extra = 1
    fields = ['body']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.user == request.user:
            kwargs["queryset"] = kwargs.get("queryset", db_field.remote_field.model.objects).exclude(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['host', 'topic', 'name',  'date_created', 'date_updated']
    search_fields = ['host', 'topic', 'name']
    list_editable = ['name', 'topic']
    list_display_links = ['host']
    readonly_fields = ['host']
    list_filter = ['host', 'topic', 'date_created', 'date_updated']
    fieldsets = (
        ('Host Detials', {
            "fields": (
                ['topic']
            ),
        }),
        ('Room Detials', {
            "fields": (
                ['name', 'description', "participant"]
            ),
        }),
    )
    inlines = [MessageInline]
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Message):
                # Set the user to the current logged-in user
                instance.user = request.user
                instance.save()
        formset.save_m2m()
        super().save_formset(request, form, formset, change)
