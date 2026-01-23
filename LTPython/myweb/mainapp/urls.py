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
    path('chat-support/', views.chatSupport, name="chat_support"),
    path('googleRedirect/', views.gooogleRedirect, name="redirect"),
    path("auth/google-login/", views.google_login, name="google_login"),
    path('custom-admin/login/', views.admin_login, name='custom_admin_login'),
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('custom-admin/logout/', views.admin_logout, name='admin_logout'),

]
