from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    listProduct = Product.objects.all()

    context = {
        'listProduct': listProduct,
    }
    return render(request, 'mainapp/home.html', context)

def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'mainapp/detail.html', {'product': product})
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
def terms(request):
    return render(request, 'mainapp/terms.html')