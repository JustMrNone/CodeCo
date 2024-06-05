from django.urls import path
from . import views
from django.shortcuts import redirect
from django.urls import reverse

urlpatterns = [
    path('', views.index, name="index"),
    path('blog', views.blog, name="blog"),
    path('Products', views.Products, name="Products"),
    path('tools', views.tools, name="tools"),
    path('settings', views.settings, name="settings"),
    path('profile', views.profile, name="profile"),
    path('cart', views.cart, name="cart"),
    path('post/<slug:slug>/', views.blogpost, name='blogpost'),
    path('accounts/login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.blog_search, name='search'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_account_settings/', views.update_account_settings, name='update_account_settings'),
    path('change_password/', views.change_password, name='change_password'),
    path('product/<int:pk>/', views.ProductDetail, name='product_detail'),
    path('product/search/', views.product_search, name='product_search'),
     path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('product_list', views.product_list, name='product_list'),
    path('finalize_order/', views.finalize_order, name='finalize_order'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('calculator', views.cal_tool, name='calculator'),
    path('colorpicker', views.colorpicker, name='colorpicker'),
    path('flatui', views.Flatui, name='flatui'),
    path('note', views.notepad, name='note'),
    path('paint', views.paint, name='paint'),
    path('todo', views.todo, name="todo"),
    path('stopwatch', views.stopwatch, name='stopwatch'),
    path('qrcode', views.generate_qr_code, name='qrcode'),
    path('pomodoro', views.pomodoro, name='pomodoro'),
    path('loremipsum', views.loremipsum, name='loremipsum'),
    path('iplocator', views.iploc, name='iplocator'),
    path('regextester', views.regextester, name='regextester'),
    path('passwordgenerator', views.passgen, name='passwordgenerator'),
    

]
