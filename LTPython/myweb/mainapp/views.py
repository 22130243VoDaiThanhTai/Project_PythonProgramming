from django.shortcuts import render

def home(request):
    return render(request, 'mainapp/home.html')
def cart(request):
    return render(request, 'mainapp/cart.html')
def introduce(request):
    return render(request, 'mainapp/introduce.html')
def contact(request):
    return render(request, 'mainapp/contact.html')
def search(request):
    return render(request, 'mainapp/search.html')
def login(request):
    return render(request, 'mainapp/login.html')
def register(request):
    return render(request, 'mainapp/register.html')
def policy(request):
    return render(request, 'mainapp/policy.html')