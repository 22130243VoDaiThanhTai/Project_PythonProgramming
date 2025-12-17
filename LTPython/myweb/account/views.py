from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from mainapp.models import Profile

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")

        return render(request, "mainapp/login.html", {
            "error": "Sai tên đăng nhập hoặc mật khẩu"
        })

    return render(request, "mainapp/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        # 1. Check password
        if password != confirm_password:
            return render(request, "mainapp/register.html", {
                "error": "Mật khẩu không khớp"
            })

        # 2. Check username tồn tại
        if User.objects.filter(username=username).exists():
            return render(request, "mainapp/register.html", {
                "error": "Tên đăng nhập đã tồn tại"
            })

        # 3. Tạo user (password được HASH tự động)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 4. Tạo profile cho user
        Profile.objects.create(
            user=user,
            address=address,
            phone=phone
        )

        # 5. Auto login sau khi đăng ký
        login(request, user)

        return redirect("home")

    return render(request, "mainapp/register.html")

def logout_view(request):
    logout(request)
    return redirect("login")
