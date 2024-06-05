from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Post, Profile, AccountSettings, Product
from .forms import RegisterForm
from .forms import CustomAuthenticationForm
from .forms import ProfileForm, AccountSettingsForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileForm, AccountSettingsForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
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
    products = Product.objects.all()
    return render(request, 'main/Products.html', {'products': products})

def ProductDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/product.html', {'product': product})


def product_search(request):
    query = request.GET.get('searchTitle', '')
    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'main/product_search_result.html', {'products': products, 'query': query})

def info(request):
    return render(request, 'main/info.html')
    


def settings(request):
    user = request.user

    # Ensure the user has a Profile and AccountSettings
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    if not hasattr(user, 'accountsettings'):
        AccountSettings.objects.create(user=user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile, user=user)
        password_form = PasswordChangeForm(user, request.POST)
        account_settings_form = AccountSettingsForm(request.POST, instance=user.accountsettings)

        if 'update_profile' in request.POST and profile_form.is_valid():
            user.username = profile_form.cleaned_data['username']
            user.email = profile_form.cleaned_data['email']
            user.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('settings')
        if 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('settings')
        if 'update_account_settings' in request.POST and account_settings_form.is_valid():
            account_settings_form.save()
            messages.success(request, 'Account settings updated successfully.')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = ProfileForm(instance=user.profile, user=user)
        password_form = PasswordChangeForm(user)
        account_settings_form = AccountSettingsForm(instance=user.accountsettings)

    return render(request, 'main/settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'account_settings_form': account_settings_form,
    })
    
    
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    
    # Render the settings page with the form, ensuring all other forms and content are included
    return render(request, 'main/settings.html', {
        'password_form': form,
        'profile_form': ProfileForm(instance=request.user.profile),
        'account_settings_form': AccountSettingsForm(instance=request.user.profile),
    })
    
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
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home page after login
    else:
        form = CustomAuthenticationForm()  # Use CustomAuthenticationForm here too
    return render(request, 'main/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to home page or login page after logout


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    return redirect('settings')

@login_required
def update_account_settings(request):
    if request.method == 'POST':
        account_settings_form = AccountSettingsForm(request.POST, instance=request.user.accountsettings)
        if account_settings_form.is_valid():
            account_settings_form.save()
            messages.success(request, 'Account settings updated successfully.')
        else:
            for field, errors in account_settings_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    return redirect('settings')


def blog_search(request):
    option = request.GET.get('option', 'title')
    query = request.GET.get('query', '')
    results = []

    if query:
        if option == 'title':
            results = Post.objects.filter(title__icontains=query)
        elif option == 'category':
            results = Post.objects.filter(categories__name__icontains=query)
        elif option == 'word':
            results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains(query)))
        message = f'Search result for "{query}" in {option}'
    else:
        message = 'Please enter a search term'

    context = {
        'results': results,
        'message': message,
        'query': query,
        'option': option
    }
    return render(request, 'main/blog_search_result.html', context)