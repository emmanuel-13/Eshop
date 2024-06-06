from django.shortcuts import redirect, render
from .models import *
from django.db.models import Q
from django.utils import timezone
from .forms import *
from django.core.paginator import Paginator

# Create your views here.
def blog(request):
    new = request.GET.get('variant') if request.GET.get('variant') != None else ''
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if new: 
        news = News.objects.filter(Q(title=new))
        blog = Blog.objects.filter(Q(new__title=new))
        recent_blog = Blog.objects.filter(Q(new__title=new), date_created__gte=timezone.now().date())[:2]
        paginator = Paginator(blog, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(news)
        
    elif q:
        news = News.objects.filter(Q(title__icontains=q))
        blog = Blog.objects.filter(Q(author__username__icontains=q)| Q(topic__icontains=q)| Q(new__title__icontains=q))
        recent_blog = Blog.objects.filter(Q(author__username__icontains=q), date_created__gte=timezone.now().date())[:2]
        paginator = Paginator(blog, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(news)
    else: 
        news = News.objects.all()
        blog = Blog.objects.all()
        recent_blog = Blog.objects.filter(date_created__gte=timezone.now().date())[:2]
        paginator = Paginator(blog, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(news)
    return render(request, 'blog/blog.html', {'new': news, 'blog': blog, 'recent': recent_blog, "page_obj": page_obj})

def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    others = Blog.objects.filter(new__title=blog.new.title)
    recent_blog = Blog.objects.filter(date_created__gte=timezone.now().date())[:4]
    
    form = CommentForm()
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=True)
            data.user = request.user
            data.blog = blog
            data.new = blog.new
            data.save()
            return redirect(blog.get_absolute_url())
        
    return render(request, 'blog/blog-details.html', {'blog': blog, "others": others, 
                                                      'recent': recent_blog, 'form': form})