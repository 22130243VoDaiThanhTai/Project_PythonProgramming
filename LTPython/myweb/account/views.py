from django.shortcuts import render, redirect
from mainapp.models import Account

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            account = Account.objects.get(username=username, password=password)

            # ✅ LƯU SESSION
            request.session['account_id'] = account.id
            request.session['username'] = account.username
            request.session['userID'] = account.userID

            return redirect('home')

        except Account.DoesNotExist:
            return render(request, 'mainapp/login.html', {
                'error': 'Sai tên đăng nhập hoặc mật khẩu'
            })

    return render(request, 'mainapp/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('home')

def register(request):
    if request.method == 'GET':
        return render(request, 'mainapp/register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 1️⃣ CHECK RỖNG
        if not all([username, email, address, phone, password, confirm_password]):
            return render(request, 'mainapp/register.html', {
                'error': 'Vui lòng nhập đầy đủ thông tin'
            })

        # 2️⃣ CHECK PASSWORD MATCH
        if password != confirm_password:
            return render(request, 'mainapp/register.html', {
                'error': 'Mật khẩu nhập lại không khớp'
            })

        # 3️⃣ CHECK TRÙNG USERNAME
        if Account.objects.filter(username=username).exists():
            return render(request, 'mainapp/register.html', {
                'error': 'Tên đăng nhập đã tồn tại'
            })

        # 4️⃣ CHECK TRÙNG EMAIL
        if Account.objects.filter(email=email).exists():
            return render(request, 'mainapp/register.html', {
                'error': 'Email đã được sử dụng'
            })

        # 5️⃣ CREATE ACCOUNT
        Account.objects.create(
            username=username,
            password=password,
            email=email,
            address=address,
            userID=1,
            phone=phone,
        )

        return redirect('login')