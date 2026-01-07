# mainapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F

# --- PROFILE USER ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

# --- DANH MỤC ---
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Danh mục sản phẩm"


# --- SẢN PHẨM ---
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    price = models.PositiveIntegerField(verbose_name="Giá bán")
    stock = models.PositiveIntegerField(default=0, verbose_name="Tồn kho")

    # 👉 chỉ lưu tên file, ví dụ: iphone15.webp
    image = models.CharField(
        max_length=255,
        blank=True,
        default="no-image.png",
        verbose_name="Ảnh sản phẩm",
        help_text="Nhập tên file trong static/images/"
    )


    active = models.BooleanField(default=True, verbose_name="Đang bán")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Kho hàng"


# --- ĐƠN HÀNG ---
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'),
        ('shipping', 'Đang giao hàng'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Khách hàng")
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    full_name = models.CharField(max_length=255, blank=True, verbose_name="Tên người nhận")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    address = models.CharField(max_length=255, blank=True, verbose_name="Địa chỉ giao hàng")
    note = models.TextField(blank=True, verbose_name="Ghi chú")

    @property
    def total_bill(self):
        return self.items.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0

    def __str__(self):
        return f"Đơn #{self.id}"

    class Meta:
        verbose_name_plural = "1. Quản lý Đơn hàng"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()     # giá tại thời điểm mua
    quantity = models.PositiveIntegerField(default=1)


# --- BÁO CÁO DOANH THU ---
class RevenueReport(Order):
    class Meta:
        proxy = True
        verbose_name = "Báo cáo Doanh thu"
        verbose_name_plural = "2. Báo cáo Doanh thu"
