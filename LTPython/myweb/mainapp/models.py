from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F

# --- CÁC MODEL CƠ BẢN (Sản phẩm vẫn phải có ngầm để bán hàng) ---
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Danh mục sản phẩm"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    price = models.IntegerField(verbose_name="Giá bán")
    stock = models.IntegerField(default=0, verbose_name="Tồn kho")
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name="Đang bán")

    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Kho hàng"

# --- MODEL QUẢN LÝ ĐƠN HÀNG ---
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'),
        ('shipping', 'Đang giao hàng'),
        ('completed', 'Đã hoàn thành (Tính doanh thu)'),
        ('cancelled', 'Đã hủy'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Khách hàng")
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")

    @property
    def total_bill(self):
        # Tính tổng tiền của đơn hàng
        total = 0
        for item in self.orderitem_set.all():
            total += item.product.price * item.quantity
        return total

    def __str__(self): return f"Đơn #{self.id}"
    class Meta: verbose_name_plural = "1. Quản lý Đơn hàng"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

# --- MODEL BÁO CÁO DOANH THU (PROXY MODEL) ---
class RevenueReport(Order):
    class Meta:
        proxy = True # Không tạo bảng mới trong DB, chỉ dùng để hiển thị admin
        verbose_name = "Báo cáo Doanh thu"
        verbose_name_plural = "2. Báo cáo Doanh thu"