from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db.models import Q, Sum
from .models import Product, Category, Profile, Order
from django.core.files.storage import default_storage
from django.db.models import Sum, F
from .models import Order, OrderItem

from AI_model.ai_model import predict_image
from django.conf import settings
import os
from django.http import JsonResponse
from urllib.parse import urlencode
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='custom_admin_login')
def admin_dashboard(request):
    users = User.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all().order_by('-date_ordered')

   
    total_revenue = OrderItem.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    context = {
        'users': users,
        'products': products,
        'orders': orders,

        'total_users': users.count(),
        'total_products': products.count(),
        'total_orders': orders.count(),
        'total_revenue': total_revenue,

        'chart_labels': ['T1', 'T2', 'T3', 'T4'],
        'chart_data': [0, 0, 0, 0],
    }

    return render(request, 'mainapp/admin_dashboard.html', context)



def home(request):
    listProduct = Product.objects.all()

    return render(request, 'mainapp/home.html', {
        'listProduct': listProduct,
    })

def admin_logout(request):
    logout(request)
    return redirect('home')

def admin_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu")
            return render(request, 'mainapp/admin_login.html')


        if user.is_staff or user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Bạn không có quyền truy cập Admin")
            return render(request, 'mainapp/admin_login.html')

    return render(request, 'mainapp/admin_login.html')

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
    keyword = request.GET.get('searched', '').strip()
    category_id = request.GET.get('category', '').strip()

    listProductSearched = Product.objects.none()

    if category_id:
        listProductSearched = Product.objects.filter(
            category_id=category_id,
            active=True
        )
    elif keyword:
        listProductSearched = Product.objects.filter(
            name__icontains=keyword,
            active=True
        )

    context = {
        'listProductSearched': listProductSearched
    }

    return render(request, 'mainapp/search.html', context)

def login_view(request):
    return render(request, 'mainapp/login.html')
def register(request):
    return render(request, 'mainapp/register.html')
def policy(request):
    return render(request, 'mainapp/policy.html')
def terms(request):
    return render(request, 'mainapp/terms.html')
def gooogleRedirect(request):
    return render(request, 'mainapp/googleRedirect.html')
def chatSupport(request):
    SEARCH_BASE = "/search/?"

    PRODUCT_CATEGORY = {
        "aothun": 2,
        "hoodie": 2,
        "bottle": 1,
        "lego": 3,
        "other": None
    }

    PRODUCT_DESC = {
        "aothun": "áo thun",
        "hoodie": "hoodie",
        "bottle": "bình giữ nhiệt",
        "lego": "lego",
        "other": "sản phẩm khác"
    }

    if request.method == "POST" and request.FILES.get("image"):
        img_file = request.FILES["image"]

        save_path = default_storage.save(f"uploads/{img_file.name}", img_file)
        full_path = os.path.join(settings.MEDIA_ROOT, save_path)

        label, confidence = predict_image(full_path)

        category_id = PRODUCT_CATEGORY.get(label)
        desc = PRODUCT_DESC.get(label, "sản phẩm")

        if category_id:
            query_params = urlencode({"category": category_id})
            search_url = f"{SEARCH_BASE}{query_params}"
            reply_text = (
                f"Mình nhận thấy sản phẩm là {desc}. "
                f"Shop có bán sản phẩm này, bạn có thể xem tại <a href='{search_url}'>đây</a>."
            )
        else:
            reply_text = "Shop mình hiện chưa bán sản phẩm này."

        return JsonResponse({
            "reply": reply_text,
            "label": label,
            "confidence": confidence
        })

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )

@csrf_exempt
def google_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)

    email = data.get("email")
    full_name = data.get("fullName", "")

    if not email:
        return JsonResponse({"error": "Missing email"}, status=400)

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": email,
            "first_name": full_name,
        }
    )

    if created:
        user.set_unusable_password()
        user.save()

        Profile.objects.create(user=user)

    login(request, user)

    return JsonResponse({
        "message": "Login Google thành công",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.first_name,
        }
    })
