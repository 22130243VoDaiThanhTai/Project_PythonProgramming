# MixiShop – Django E-commerce Project

MixiShop là website bán hàng mô phỏng (đồ án), gồm:

- Trang người dùng: xem sản phẩm, giỏ hàng, đặt hàng  
- Admin custom (tự xây dựng, KHÔNG dùng Django Admin mặc định)  
- Quản lý sản phẩm, người dùng, đơn hàng  
- Tích hợp AI (TensorFlow) để demo nhận diện ảnh  

---

## I. YÊU CẦU HỆ THỐNG

- Windows (khuyến nghị)
- Python **3.9** (**bắt buộc nếu dùng AI / TensorFlow**)
- pip
- PowerShell
- Git

⚠️ **KHÔNG dùng Python 3.12 / 3.13** (TensorFlow không hỗ trợ ổn định)

---

## II. CLONE PROJECT

```bash
git clone <repo-url>
cd LTPython/myweb

A. TẠO & KÍCH HOẠT VIRTUAL ENVIRONMENT (BẮT BUỘC)
1. Tạo virtual environment
py -3.9 -m venv venv39

2. Kích hoạt venv (PowerShell)
.\venv39\Scripts\activate
B. CÀI ĐẶT THƯ VIỆN
pip install django django-jazzmin pillow pymysql tensorflow
C. MIGRATE DATABASE
python manage.py makemigrations
python manage.py migrate
D. TẠO TÀI KHOẢN ADMIN
python manage.py createsuperuser
E. SEED DỮ LIỆU MẪU
python manage.py seed
F. CHẠY SERVER
python manage.py runserver
