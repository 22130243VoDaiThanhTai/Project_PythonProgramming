# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from mainapp.models import Category, Product


class Command(BaseCommand):
    help = "Seed demo data for MixiShop"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Seeding data...")

        Product.objects.all().delete()
        Category.objects.all().delete()

        c1 = Category.objects.create(name="Cốc bình")
        c2 = Category.objects.create(name="Áo Mixi")
        c3 = Category.objects.create(name="Lego")

        products = [
            ("Cốc Mixi 1200ml", "coc-mixi-1200ml.webp", 250000, 100, c1), 
            ("Bình giữ nhiệt Mixi", "binh-giu-nhiet-mixi.webp", 190000, 100, c1), 
            ("Bình giữ nhiệt Fan cứng Mixi", "binh-giu-nhiet-fan-cung-mixi.webp", 170000, 100, c1), 
            ("Áo hoodie Mixi đen khóa ngực", "ao-hoodie-mixi-den-khoa-nguc.webp", 500000, 100, c2), 
            ("Áo khoác Mixi đen", "ao-khoac-mixi-den.webp", 500000, 100, c2), 
            ("Áo phông Mixi - Tộc Trưởng", "ao-phong-mixi-toc-truong.webp", 149000, 100, c2), 
            ("Áo phông Mixi - Phòng Stream", "ao-phong-mixi-phong-stream.webp", 149000, 100, c2), 
            ("Áo phông Mixi - Trắng", "ao-phong-mixi-trang.webp", 220000, 100, c2), 
            ("Áo phông Mixi logo - Đen", "ao-phong-mixi-logo-den.webp", 250000, 100, c2), 
            ("Áo Sologan MixiGaming 2024", "ao-sologan-mixigaming-2024.webp", 250000, 100, c2), 
            ("Áo logo 2023", "ao-logo-2023.webp", 250000, 100, c2), ("Áo nỉ dài tay Mixi", "ao-ni-dai-tay-mixi.webp", 350000, 100, c2), 
            ("Áo nỉ dài tay MixiCity", "ao-ni-dai-tay-mixicity.webp", 350000, 100, c2), ("Áo nỉ dài tay MXG - Đen", "ao-ni-dai-tay-mxg-den.webp", 350000, 100, c2), 
            ("Lego Mixi Block SS1", "lego-mixi-block-ss1.webp", 350000, 100, c3), ("Lego Mixi Block SS2", "lego-mixi-block-ss2.webp", 350000, 100, c3), 
            ("Lego Mixi Block SS3", "lego-mixi-block-ss3.webp", 350000, 100, c3), ("Lego Mixi Block SS4", "lego-mixi-block-ss4.webp", 350000, 100, c3), 
            ("Lego Mixi Block SS5", "lego-mixi-block-ss5.webp", 350000, 100, c3), ("Lego Mixi Block SS6", "lego-mixi-block-ss6.webp", 350000, 100, c3), 
            ("Lego Mixi Block SS7", "lego-mixi-block-ss7.webp", 350000, 100, c3), ("Lego Mixi Block SS8", "lego-mixi-block-ss8.webp", 350000, 100, c3), 
            ("Lego Mixi Block SS9", "lego-mixi-block-ss9.webp", 35000, 100, c3),
        ]

        for name, image, price, stock, category in products:
            Product.objects.create(
                name=name,
                price=price,
                stock=stock,
                category=category,
                image=image,
                active=True
            )

        self.stdout.write(self.style.SUCCESS("✅ Seed data thành công!"))
