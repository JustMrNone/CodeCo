from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Post, User
from .forms import RegisterForm

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def blog(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)
    
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
  
    
    return render(request, 'main/blog.html', {
        'posts': posts
    })

def blogpost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'main/blogpost.html', {'post': post})


def Products(request):
    return render(request, 'main/Products.html')

def info(request):
    return render(request, 'main/info.html')
    
def settings(request):
    return render(request, 'main/settings.html')

@login_required
def profile(request):
    return render(request, 'main/profile.html')

def cart(request):
    return render(request, 'main/cart.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # Authentication failed for some reason
                return redirect('register')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to home page or login page after logout