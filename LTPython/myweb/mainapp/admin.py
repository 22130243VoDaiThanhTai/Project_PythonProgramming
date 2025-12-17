from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from .models import Order, OrderItem, RevenueReport, Product, Category

admin.site.unregister(Group)

# Inline để xem sản phẩm trong đơn
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('thanh_tien',)
    def thanh_tien(self, obj):
        return f"{obj.product.price * obj.quantity:,} VNĐ"

# 2. QUẢN LÝ ĐƠN HÀNG
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # --- SỬA LỖI Ở DÒNG DƯỚI ĐÂY ---
    # Thay 'status_color' thành 'status' để khớp với list_editable
    list_display = ('id', 'customer', 'date_ordered', 'status', 'total_display')

    list_filter = ('status', 'date_ordered')
    list_editable = ('status',) # Cho phép đổi trạng thái nhanh bằng menu thả xuống
    inlines = [OrderItemInline]

    def total_display(self, obj):
        return f"{obj.total_bill:,} VNĐ"
    total_display.short_description = "Tổng tiền"

# 3. BÁO CÁO DOANH THU (Chỉ xem, không sửa)
@admin.register(RevenueReport)
class RevenueReportAdmin(admin.ModelAdmin):
    list_display = ('date_ordered', 'customer', 'doanh_thu_don')
    list_filter = ('date_ordered',)

    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='completed')

    def doanh_thu_don(self, obj):
        return f"+ {obj.total_bill:,} VNĐ"
    doanh_thu_don.short_description = "Thực thu"

# Đăng ký các phần phụ
admin.site.register(Product)
admin.site.register(Category)