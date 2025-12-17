from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from mainapp.models import Product, Order, OrderItem

# Lấy hoặc tạo giỏ hàng
def get_cart(user):
    cart, created = Order.objects.get_or_create(
        customer=user,
        status='pending'
    )
    print(f"Cart ID: {cart.id}, Created: {created}, Items: {cart.items.count()}")
    return cart

@login_required
def cart_detail(request):
    cart = get_cart(request.user)
    items = cart.items.select_related('product').all()

    item_list = []
    total = 0
    for item in items:
        subtotal = item.price * item.quantity
        total += subtotal
        item_list.append({
            'id': item.id,
            'product': item.product,
            'price': item.price,
            'quantity': item.quantity,
            'subtotal': subtotal
        })

    # DEBUG
    print("DEBUG: Cart items:", item_list)

    return render(request, 'mainapp/cart.html', {
        'cart': cart,
        'items': item_list,
        'total': total
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, active=True)

    if product.stock <= 0:
        return redirect('home')

    cart = get_cart(request.user)

    item, created = OrderItem.objects.get_or_create(
        order=cart,
        product=product,
        defaults={
            'price': product.price,
            'quantity': 1
        }
    )

    if not created:
        if item.quantity < product.stock:
            item.quantity += 1

    item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        OrderItem,
        id=item_id,
        order__customer=request.user
    )
    item.delete()
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        item = get_object_or_404(
            OrderItem,
            id=item_id,
            order__customer=request.user
        )

        if quantity > 0:
            item.quantity = min(quantity, item.product.stock)
            item.save()
        else:
            item.delete()

    return redirect('cart')
