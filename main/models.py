from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone 
from django.urls import reverse 
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, *kwargs)
    
    def get_absolute_url(self):
        return reverse("tag_detail", args=[self.slug])
    

class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    
    class Meta:
        ordering = ['-published_date']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs) 
            
        

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField() 
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['created_on']
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'   
    
