from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('introduce/', views.introduce, name='introduce'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('policy/', views.policy, name='policy'),
    path('terms/', views.terms, name='terms'),
    path('product/<int:product_id>/', views.detail, name='detail'),
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls')),
]
