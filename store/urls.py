from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product_details/', views.product_details, name='product_details'),
    path('cart/', views.cart, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Include this line
    path('logout/', views.user_logout, name='logout'),
    
]
