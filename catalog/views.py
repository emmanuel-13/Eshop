from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from auths.forms import UserForm2, CustomerForm
from auths.models import Customer
from blog.models import *
from django.core.paginator import Paginator
from .forms import ProductReviewForm
# Create your views here.

def home(request):
    category = Category.objects.all()[:10]
    product = Product.objects.filter(date_created__gte=timezone.now().date())
    top_rated = Product.objects.filter(top_rated=True)
    blog = Blog.objects.all().order_by("-date_updated")[:3]
    return render(request, 'index.html', {"category": category, 'product': product, 
                                          'top_rated': top_rated, 'blog': blog})

def shop(request):
    variant = request.GET.get('variant') if request.GET.get('variant') != None else ''
    sub = request.GET.get('sub') if request.GET.get('sub') != None else ''
    bd = request.GET.get('brand') if request.GET.get('brand') != None else ''
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print(q)
    if q:
        brand = Brand.objects.filter(Q(category__name__icontains=q)|Q(subcat__name__icontains=q))   
        subcat = SubCat.objects.filter(Q(category__name__icontains=q))
        pro = Product.objects.filter(date_created__gte=timezone.now().date())
        product = Product.objects.filter(Q(category__name__icontains=q)|Q(subcat__name__icontains=q)|Q(brand__name__icontains=q))
        print(subcat,brand, product)
        paginator = Paginator(product, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop-grid.html', {'product': product, 'brand': brand,
                                              'pro': pro, 'subcat': subcat, 'page_obj': page_obj })
        
    elif variant or sub or bd:
        brand = Brand.objects.filter(Q(category__name=variant)|Q(subcat__name=sub)|Q(category__name=sub)|Q(subcat__name=variant))
        subcat = SubCat.objects.filter(Q(category__name=variant)|Q(category__name=sub))
        pro = Product.objects.filter(date_created__gte=timezone.now().date())
        product = Product.objects.filter(Q(category__name=variant)|Q(subcat__name=sub)|Q(brand__name=bd))
        paginator = Paginator(product, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop-grid.html', {'product': product, 'brand': brand,
                                              'pro': pro, 'subcat': subcat, 'page_obj': page_obj })
        
    else:
        product = Product.objects.all()
        brand = Brand.objects.all().order_by('-date_updated')[:6]
        pro = Product.objects.filter(date_created__gte=timezone.now().date())
        subcat = SubCat.objects.all()
        paginator = Paginator(product, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop-grid.html', {'product': product, 'brand': brand,
                                              'pro': pro, 'subcat': subcat, 'page_obj': page_obj })
    
def shop_details(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        
        if request.user.is_authenticated:
            view, _ = RecentView.objects.get_or_create(user=request.user)
            view.product.add(product)
            view.save()
        else:
            pass
        related_product = Product.objects.filter(category__name=product.category)
        form = ProductReviewForm()
        return render(request, 'shop-details.html', {'pro': product, 'related_product': related_product,
                                                      "form": form})
    except Exception as e:
        messages.info(request, e)
        return redirect('home')

def checkout(request):
    
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cartitems = CartProduct.objects.filter(cart__user=cart.user, cart__is_paid=False)
        
        if cart:
            customer = Customer.objects.filter(user=request.user).first()
            check_user = User.objects.get(username=request.user.username)
            
            print(customer)
            
            if customer:
                form = CustomerForm(instance=customer)
                myuser = UserForm2(instance=request.user)
                
                if request.method == "POST":
                    form = CustomerForm(request.POST, instance=customer)
                    myuser = UserForm2(request.POST, instance=request.user)
                    
                    if form.is_valid() and myuser.is_valid():
                        user_data = myuser.save()
                        customer_data = form.save()
                        
                        print(cart.ref)
                        amount = round(cart.get_cart_total_tax(), 2)
                        print(int(amount))
                        return render(request, 'make_payment.html', {'customer_data': customer_data, 'user_data': user_data,
                                                                     "cart": cart, 'cart_product': cartitems, 'amount': int(amount), 'pay_key': settings.PAYSTACK_PUBLIC_KEY })

                        # # for product in cartitems:
                        # #     print(product)
                        # #     Purchase.objects.create(cart=product)
                        # # cart.is_paid = True
                        # # cart.save()
                        # return redirect("success")
        
            else:
                if check_user.email or check_user.phone_number:
                    print(check_user.id)
                    form = CustomerForm()
                    myuser = UserForm2(instance=request.user)
                    
                    if request.method == "POST":
                        form = CustomerForm(request.POST)
                        myuser = UserForm2(request.POST, instance=request.user)
                        
                        if form.is_valid() and myuser.is_valid():
                            usr = myuser.save()
                            cus = form.save(commit=False)
                            cus.user_id = usr.id
                            cus.save()
                            
                        # print(customer_data.ref)
                            return render(request, 'make_payment.html', {'customer_data': cus, 'user_data': usr,
                                                                     "cart": cart, 'cart_product': cartitems, 'pay_key': settings.PAYSTACK_PUBLIC_KEY })
                else:
                    form = CustomerForm()
                    myuser = UserForm2()
                    
                    if request.method == "POST":
                        form = CustomerForm(request.POST)
                        myuser = UserForm2(request.POST)
                        
                        if form.is_valid() and myuser.is_valid():
                            user = myuser.save()
                            cus = form.save(commit=False)
                            cus.user_id = user.id
                            cus.save()
                            
                            return render(request, 'make_payment.html', {'customer_data': cus, 'user_data': usr,
                                                                     "cart": cart, 'cart_product': cartitems, 'pay_key': settings.PAYSTACK_PUBLIC_KEY })
            context = {'cartitems': cartitems, 'cart': cart, 'form': form, 'myuser': myuser}
            return render(request, "checkout.html", context)
        else:
            return redirect("shop")
    except Exception as e:
        messages.info(request, e)
        return redirect("shop")

# @login_required
def verify_payment(request, ref):
    cart = get_object_or_404(Cart, ref=ref)
    if cart:
        cartitems = CartProduct.objects.filter(cart__user=request.user, cart__is_paid=False)
        confirm = cart.verify_payment()
        print(confirm)
        
        if confirm:
            cartitems = CartProduct.objects.filter(cart__user=request.user, cart__is_paid=False)
            for product in cartitems:
                Purchase.objects.create(cart=product)
                
            cart.is_paid = confirm
            cart.save()
        
            messages.success(request, 'payment verify successfully')
            return redirect('success')
        else:
            messages.success(request, 'payment failed verification')
            return redirect('checkout')
    else:
        messages.error(request, 'verifcation not complete')
    return redirect('checkout')

def success(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please Login!!!')
        return redirect('login')
    else:
        cart = Cart.objects.filter(user=request.user, is_paid=True).first()
        if cart:
            return render(request, 'success.html')
        else:
            return redirect("checkout")

def cart_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_product = CartProduct.objects.filter(cart__user=cart.user, cart__is_paid=False)
        print(cart_product)
        return render(request, "shoping-cart.html", {'cart_product': cart_product, 'cart': cart})
    else:
        messages.info(request, 'you are not allowed, Please Login')
        return redirect(request.META.get("HTTP_REFERER"))

def cart_add(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=pk)
        
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_product.quantity += 1
            cart_product.save()
            messages.success(request, f"{product} has been added in your cart")
        elif cart_product:
            cart_product.quantity += 1
            cart_product.save()
            messages.info(request, f"{product} updated to cart")
        else:
            pass
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.info(request, "yo!, you can\'t add product to cart with login")
        return redirect(request.META.get("HTTP_REFERER"))
    
def cart_delete(request, id):
    if request.user.is_authenticated:
        cart_product = CartProduct.objects.get(id=id)
        cart_product.delete()
        return redirect('cart_view')
    else:
        messages.info(request, "Yo!!, Kindly login to continue...")
        return redirect(request.META.get("HTTP_REFERER"))

def cart_update(request, id):
    cart_product = CartProduct.objects.get(id=id)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        
        if new_quantity == 0:
            pass
        elif new_quantity >= 0:
            if cart_product.quantity > new_quantity:
                cart_product.quantity = new_quantity
                cart_product.save()
                messages.success(request, "Quantity has been updated successfully")
            else:
                cart_product.quantity = new_quantity
                cart_product.save()
                messages.success(request, "Product Quantity exceeded quantity limit")
    else:
        messages.info(request, "quantity cannot be less than zero(0)")
    return redirect('cart_view')


def product_review(request):
    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        print(form.errors)
        
        if form.is_valid():
            name = request.POST.get('name', None)
            content = request.POST.get('content', None)
            product = request.POST.get('product', None)
            print(content, product)
            
            review = Review(content=content, name=name, product=int(product))
            review.save()
            
            print("i have been created successfully again")
            return JsonResponse({"status": "data saved successfully"}, safe=False)
        return JsonResponse({"status": "unable to save"}, safe=False)
            