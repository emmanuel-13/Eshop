from django.db import models
from django.urls import reverse
from auths.models import User
from ckeditor.fields import RichTextField
from PIL import Image
from django.utils.text import slugify

news = (
    ('Life', 'life'), ('Movies', 'movies')
)

class News(models.Model):
    title = models.CharField(max_length=255, choices=news, default=news[0][0])
    slug = models.SlugField(editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "New"
        verbose_name_plural = "News"
        ordering = (('-date_created', '-date_updated',))
        
    def get_blog_total(self):
        blogs = self.blog_set.all().count()

        return blogs
    
    def get_comment_total(self):
        comment = self.comment_set.all().count()
        return comment
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    new = models.ForeignKey(News, on_delete=models.CASCADE, default="1")
    image = models.ImageField(upload_to='blog-image/', default='../static/images/bg-themes/5.png', null=True, blank=True)
    topic = models.CharField(max_length=200, verbose_name="blog-topic")
    slug = models.SlugField(editable=False)
    descriptions = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height >= 315 and img.width >= 360:
            output = (315, 360)
            img.thumbnail(output)
            img.save(self.image.path)
    
    def __str__(self) -> str:
        return self.topic
    
    def get_comment_total(self):
        comments = self.comment_set.all().count()
        return comments
    
    def get_absolute_url(self):
        return reverse("blog_details", kwargs={"slug": self.slug})
    
        

class Comment(models.Model):
    new = models.ForeignKey(News, on_delete=models.CASCADE, default="1")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.comment
    
    class Meta:
        ordering = ['-date_updated', '-date_created']
    