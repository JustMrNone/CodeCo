from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('blog', views.blog, name="blog"),
    path('Products', views.Products, name="Products"),
    path('info', views.info, name="info"),
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
    path('change_password/', views.change_password, name='change_password')
    
]
