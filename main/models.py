from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone 
from django.urls import reverse 
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    

class AccountSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_newsletter = models.BooleanField(default=True)
    two_factor_auth = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

# Signal to create or update Profile whenever User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    


class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', default='settings/img/Sample.png')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.user.username}'

    def total_price(self):
        return sum(item.total_price() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    def total_price(self):
        return self.quantity * self.product.price