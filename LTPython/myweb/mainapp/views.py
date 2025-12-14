from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    listProduct = Product.objects.all()

    # ✅ CHECK LOGIN
    is_login = request.session.get('account_id') is not None

    return render(request, 'mainapp/home.html', {
        'listProduct': listProduct,
        'is_login': is_login
    })

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
def login_view(request):
    return render(request, 'mainapp/login.html')
def register(request):
    return render(request, 'mainapp/register.html')
def policy(request):
    return render(request, 'mainapp/policy.html')
def terms(request):
    return render(request, 'mainapp/terms.html')