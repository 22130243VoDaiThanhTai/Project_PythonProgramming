from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'), 
    path('introduce/', views.introduce, name='introduce'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    
]
