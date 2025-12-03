from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'), 
    path('introduce/', views.introduce, name='introduce'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('policy/', views.policy, name='policy'),
    path('terms/', views.terms, name='terms'),
    
]
