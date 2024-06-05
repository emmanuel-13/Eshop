from typing import Any
from django.contrib import admin
from .models import *

# Register your models here.

class BlogInline(admin.StackedInline):
    model = Blog
    extra = 1
    exclude = ['author']

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    exclude = ['user']
    
    def has_add_permission(self, request, obj=None):
        if obj:
            return True
        return False
    
    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        print(obj)
        formset.form.base_fields['blog'].queryset = Blog.objects.filter(new__title=obj)
        return formset
    
@admin.register(News)
class NewAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'date_updated', 'get_blog_total', 'get_comment_total']
    # list_editable = ['news']
    list_filter = ['title', 'date_created', 'date_updated']
    search_fields = ['title']
    inlines = [BlogInline, CommentInline]
    
    def save_formset(self, request, form, formset, change):
        if formset.model == Comment:
            # Get the subcategory id from the SubcategoryInline formset
            news = form.instance
            
            if news.blog_set.exists():
                blog_id = news.blog_set.first()
                blog_id.author_id = request.user.id
                blog_id = blog_id.id
            
                for form in formset.forms:
                    if form.instance.pk is None:
                        form.instance.blog_id = blog_id
                        form.instance.user_id = request.user.id
        formset.save()
        
        if formset.model == Blog:
            news = form.instance
            print(news.id)
            
            for form in formset.forms:
                    print(form.instance.id, form.instance.author_id)
                    if form.instance.pk is None:
                        form.instance.new_id = news.id
                        form.instance.author_id = request.user.id
        formset.save()


class CommentInline2(admin.TabularInline):
    model = Comment
    extra = 1
    exclude = ['user', 'new']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['author', 'topic', 'image', 'date_created', 'date_updated', 'get_comment_total']
    list_filter = ['topic', 'date_created', 'date_updated']
    search_fields = ['topic', 'get_comment_total']
    inlines = [CommentInline2]
    exclude = ['comment']
    fieldsets = (
        (None, {
            "fields": (
                'new', 'topic',
            ),
        }),
        
        ("Blog Details", {
            "fields": (
                'descriptions', 'image',
            ),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Comment):
                # Set the user to the current logged-in user
                instance.user = request.user
                instance.save()
        formset.save_m2m()
        super().save_formset(request, form, formset, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'comment', 'date_created', 'date_updated']
    exclude = ['user']
    list_editable = ['comment']
    list_filter = ['user', 'blog', 'date_created', 'date_updated']
    search_fields = ['user', 'blog', 'comment']
    list_per_page = 5
    list_max_show_all = 10
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)
    
    
    