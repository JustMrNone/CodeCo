from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Post, Profile, AccountSettings, Product, Cart, CartItem
from .forms import RegisterForm
from .forms import CustomAuthenticationForm
from .forms import ProfileForm, AccountSettingsForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileForm, AccountSettingsForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import qrcode
from io import BytesIO
import base64
# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def blog(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)
    
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'main/blog.html', {'posts': posts, 'page_obj': posts})
def blogpost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'main/blogpost.html', {'post': post})


def Products(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 12)  # Show 10 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/Products.html', {'page_obj': page_obj})
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

def tools(request):
    return render(request, 'main/tools.html')
    


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
            results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
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


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'main/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))  # Default quantity is 1 if not provided

        # Retrieve the cart item
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        # Update the quantity
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True, 'message': 'Cart item updated successfully'})
        else:
            # If quantity is 0 or negative, remove the item from the cart
            cart_item.delete()
            return JsonResponse({'success': True, 'message': 'Cart item removed successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        cart_total = 0.0

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def finalize_order(request):
    if request.method == 'POST':
        # Handle order finalization logic here
        try:
            cart = Cart.objects.get(user=request.user)
            # Logic to create an Order and move items
            CartItem.objects.filter(cart=cart).delete()  # Clear cart
        except Cart.DoesNotExist:
            pass
        return redirect('order_success')
    return redirect('checkout')

def order_success(request):
    return render(request, 'main/order_success.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def pomodoro(request):
    return render(request, 'main/tools/pomodoro.html')
def cal_tool(request):
    return render(request, 'main/tools/calculator.html')

def colorpicker(request):
    return render(request, 'main/tools/colorpicker.html')

def Flatui(request):
    return render(request, 'main/tools/Flatuicolors.html')

def notepad(request):
    return render(request, 'main/tools/notepad.html')

def passgen(request):
    return render(request, 'main/tools/passwordgenerator.html')

def paint(request):
    return render(request, 'main/tools/paint.html')

def todo(request):
    return render(request, 'main/tools/todo.html')

def stopwatch(request):
    return render(request, 'main/tools/stopwatch.html')

def loremipsum(request):
    return render(request, 'main/tools/loremipsum.html')

def iploc(request):
    return render(request, 'main/tools/iploc.html')

def regextester(request):
    return render(request, 'main/tools/regextester.html')


def generate_qr_code(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        if data:
            img = qrcode.make(data)
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return render(request, 'main/tools/qrcode.html', {'img_base64': img_base64, 'data': data})
    return render(request, 'main/tools/qrcode.html')

