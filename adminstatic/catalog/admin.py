from collections.abc import Sequence
from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.http import HttpRequest
from .models import *
from django.forms.models import BaseInlineFormSet
from django import forms


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = "__all__"
        
#     def __init__(self, *args, **kwargs):
#         super(ProductForm, self).__init__(*args, **kwargs)
#         self.fields['subcat'].queryset = SubCat.objects.none()
#         self.fields['brand'].queryset = Brand.objects.none()
        
#         if 'category' in self.data:
#             print('yes')
#             try:
#                 category_id = int(self.data.get('category'))
#                 self.fields['subcat'].queryset = SubCat.objects.filter(category=category_id)
#                 self.fields['brand'].queryset = Brand.objects.filter(subcat__category_id=category_id)
#             except (ValueError):
#                 pass
#         elif self.instance.pk:
#             self.fields['subcat'].queryset = self.instance.category.subcat_set
#             self.fields['brand'].queryset = self.instance.subcat.brand_set


class BrandInline(admin.StackedInline):
    model = Brand
    extra = 1
    
    def has_add_permission(self, request, obj=None):
        if obj:
            return True
        return False
    
    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        print(obj)
        formset.form.base_fields['subcat'].queryset = SubCat.objects.filter(category=obj)
        return formset
  
# Register your models here.
class ProductInline(admin.StackedInline):
    model = Product
    extra = 1
    # exclude = [
    #     'subcat'
    # ]
    
    def has_add_permission(self, request, obj=None):
        if obj:
            if obj.brand_set.first() == None:
                pass
            else:
                return True
        return False
    
    # def has_change_permission(self, request, obj=None):
    #     return True
    
    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        print(obj)
        formset.form.base_fields['subcat'].queryset = SubCat.objects.filter(category=obj)
        formset.form.base_fields['brand'].queryset = Brand.objects.filter(subcat__category=obj)
        return formset

    
    class Media:
        js = ("admin/js/product_filter.js")
    
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "brand":
    #         category_id = request.GET.get("name", None)
    #         print(category_id)
    #         if category_id:
    #             kwargs['queryset'] = Brand.objects.filter(category_id=category_id)
    #         else:
    #             kwargs['queryset'] = Brand.objects.none()
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
class SubCatInline(admin.StackedInline):
    model = SubCat
    extra = 1
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['format_color_html', 'image', 'date_created', 'date_updated']
    # list_editable = ['name']
    search_fields = ['name', 'product']
    inlines = [SubCatInline, BrandInline, ProductInline]
    
    def save_formset(self, request, form, formset, change):
        if formset.model == Brand:
            # Get the subcategory id from the SubcategoryInline formset
            cat = form.instance
            # print(cat)
            # print(cat.subcat_set.first().brand_set.all())
            
            # If the category has subcategories, retrieve the first subcategory
            if cat.subcat_set.exists():
                subcat = cat.subcat_set.first()
                subcat_id = subcat.id
                
                for form in formset.forms:
                    # print(form.instance.pk, form.instance.subcat_id)
                    if form.instance.pk is None:  # New instance
                        # print(form.instance.name, form.instance.subcat_id)
                        # print(form.instance._meta.fields)``
                        
                        form.instance.subcat_id = subcat_id
            else:
                pass
            
        elif formset.model == Product:
            cat = form.instance
            # If the category has subcategories, retrieve the first subcategory
            if cat.subcat_set.exists():
                subcat = cat.subcat_set.first()
                subcat_id = subcat.id
                # print(subcat_id)
                
                # for brand in cat.subcat_set.first().brand_set.all():
                #     for product in brand.product_set.all():
                #         print(brand, product)
                
                for form in formset.forms:
                        # print(form.instance.pk, form.instance.subcat_id)
                        if form.instance.pk is None:  # New instance
                            # print(form.instance.name, form.instance.subcat_id)
                            form.instance.subcat_id = subcat_id
        formset.save()
        
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'subcat', 'brand', 'name', 'slug', 'price', 'discount', 'new_price', 'date_created', 'date_updated']
class BrandInline2(admin.StackedInline):
    model = Brand
    extra = 1
    exclude = ['category']
    
class ProductInline2(admin.StackedInline):
    model = Product
    extra = 1
    exclude = ['category']
    
    def has_add_permission(self, request, obj=None):
        if obj:
            return True
        return False
    
    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        print(obj)
        try:
            formset.form.base_fields['category'].queryset = Category.objects.get(name=obj)
        except Exception as e:
            pass
    
        try:
            formset.form.base_fields['brand'].queryset = Brand.objects.filter(subcat=obj)
            print(formset.form.base_fields['brand'].queryset.all())
        except Exception as e:
            pass
        return formset


@admin.register(SubCat)
class SubCatAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'date_created', 'date_updated']
    inlines = [BrandInline2, ProductInline2]
    
    def save_formset(self, request, form, formset, change):
        if formset.model == Product:
            # Get the subcategory id from the SubcategoryInline formset
            cat = form.instance
            print(cat)
            
            for form in formset.forms:
                print(form.instance.pk, form.instance.category_id)
                if form.instance.pk is None:  # New instance
                    # print(form.instance.name, form.instance.subcat_id)
                    form.instance.category_id = cat.category.id
                    form.instance.subcat_id = cat.id
        
    
        elif formset.model == Brand:
            # Get the subcategory id from the SubcategoryInline formset
            cat = form.instance
            print(cat)
                
            for form in formset.forms:
                print(form.instance.pk, form.instance.category_id)
                if form.instance.pk is None:  # New instance
                    form.instance.subcat_id = cat.id
                    form.instance.category_id = cat.category.id
           
        formset.save()
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['category', 'subcat', 'name', 'date_created', 'date_updated']
    inlines = [ProductInline]
    
@admin.register(Review)
class ProductReview(admin.ModelAdmin):
    list_display = ['name', 'content', 'product', 'date_created', 'date_updated' ]
    search_fields = ['name', 'product']
    list_editable = ['content']
    list_filter = ['name', 'product', 'date_created', 'date_updated']
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if obj.name == "":
            if request.user.is_authenticated:
                if request.user.first_name:
                    obj.name = request.user.get_full_name
            else:
                pass
        else:
            pass
        return super().save_model(request, obj, form, change)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['cart', 'status', 'date_created', 'date_updated']
    list_editable = ['status']
    list_filter = ['status', 'date_created', 'date_updated']
    search_fields = ('cart', )
      
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'date_updated', 'ref', 'date_created']
    list_editable = ['is_paid']
    list_filter = ['is_paid', 'date_updated', 'date_created']
    list_per_page = 10
    list_max_show_all = 100
    
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        
        if "is_paid" == False:
            custom_fields = ['get_cart_total', 'get_cart_total_tax']
            list_display += custom_fields
        
        return list_display
        # return super().get_list_display(request)
    
@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'date_updated', 'date_created', 'get_price_item', "get_cart_status"]
    list_editable = ['quantity']
    list_filter = ['date_updated', 'date_created', 'product']
    list_per_page = 10
    list_max_show_all = 100
    
@admin.register(RecentView)
class RecentViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'date_view']
    list_filter = ['user', 'date_view']
    search_fields = ['user']