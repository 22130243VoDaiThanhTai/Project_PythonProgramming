from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.files.storage import default_storage
from .models import Product, Category
from AI_model.ai_model import predict_image
from django.conf import settings
import os
from django.http import JsonResponse
from urllib.parse import urlencode

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