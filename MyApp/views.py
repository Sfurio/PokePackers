from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Card, Cart, Order, OrderItem


from django.core.mail import send_mail

import stripe
from django.conf import settings


def checkout_success_view(request):
    return render(request, 'checkout_success.html')


def checkout_view(request):
    if request.method == "POST":
        # Extract cart and form data
        cart = request.session.get('cart', {})
        total = sum(item['product'].price * item['quantity'] for item in cart.values())

        # Create Order object
        order = Order.objects.create(
            full_name=request.POST['full_name'],
            address=request.POST['address'],
            email=request.POST['email'],
            total_price=total
        )

        # Create OrderItem objects
        for product_id, quantity in cart.items():
            product = Card.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        # Clear the cart
        request.session['cart'] = {}

        # Send confirmation email
        send_mail(
            subject='Order Confirmation - PokePackers',
            message=f"Thank you for your order, {order.full_name}!\nYour total is ${order.total_price}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.email],
            fail_silently=False,
        )

        # Redirect to success page
        return redirect('checkout_success', order_id=order.id)

    # Example: Get cart from session
    cart = request.session.get('cart', {})
    total = sum(item['product'].price * item['quantity'] for item in cart.values())

    return render(request, 'checkout.html', {'cart': cart, 'total': total})
def home(request):
    images = ['sampic.JPG', 'marisite.JPG', 'WebExCode.JPG']
    return render(request, 'home.html', {'images': images})


def regular_cards(request):
    sort_by = request.GET.get('sort', 'name')  # Default sorting by name
    
    # Validate sort_by to ensure it's a valid field
    valid_sort_fields = ['name', 'price', 'set']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'  # Default to 'name' if invalid sort field

    # Filter cards where inventory is greater than 0
    cards = Card.objects.filter(type='Regular', inventory__gt=0).order_by(sort_by)

    paginator = Paginator(cards, 24)  # Show 24 cards per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'regular.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })


def reverse_cards(request):
    sort_option = request.GET.get('sort')
    
    if sort_option == 'price':
        cards = Card.objects.filter(type='Reverse', inventory__gt=0).order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='Reverse', inventory__gt=0).order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='Reverse', inventory__gt=0).order_by('name')
    else:
        cards = Card.objects.filter(type='Reverse', inventory__gt=0)

    # Pagination
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Reverse.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })


def foil_cards(request):
    sort_option = request.GET.get('sort')
    
    if sort_option == 'price':
        cards = Card.objects.filter(type='Foil', inventory__gt=0).order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='Foil', inventory__gt=0).order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='Foil', inventory__gt=0).order_by('name')
    else:
        cards = Card.objects.filter(type='Foil', inventory__gt=0)

    # Pagination
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Foil.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })


def rare_cards(request):
    sort_option = request.GET.get('sort')
    
    if sort_option == 'price':
        cards = Card.objects.filter(type='Rare', inventory__gt=0).order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='Rare', inventory__gt=0).order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='Rare', inventory__gt=0).order_by('name')
    else:
        cards = Card.objects.filter(type='Rare', inventory__gt=0)

    # Pagination
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Rare.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })


def PSA_Graded(request):
    sort_option = request.GET.get('sort')
    
    if sort_option == 'price':
        cards = Card.objects.filter(type='PSA', inventory__gt=0).order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='PSA', inventory__gt=0).order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='PSA', inventory__gt=0).order_by('name')
    elif sort_option == 'grade':
        cards = Card.objects.filter(type='PSA', inventory__gt=0).order_by('grade')
    else:
        cards = Card.objects.filter(type='PSA', inventory__gt=0)

    # Pagination
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Psa.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })


def add_to_cart(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    if card.inventory <= 0:
        # Redirect if the card has no stock
        return redirect('some_error_page_or_message')  # Replace with a suitable error page

    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Default quantity to 1 if not provided
    quantity = int(request.GET.get('quantity', 1))

    # Ensure the quantity doesn't exceed the available stock
    if quantity > card.inventory:
        quantity = card.inventory  # Set the quantity to the available stock

    # Check if item is already in the cart
    cart_item, created = Cart.objects.get_or_create(
        session_id=session_id,
        card=card,
        defaults={'quantity': quantity}
    )

    if not created:
        # If item already exists, update the quantity
        cart_item.quantity += quantity
        if cart_item.quantity > card.inventory:
            cart_item.quantity = card.inventory  # Limit to available stock
        cart_item.save()

    return redirect('cart')


def cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Filter cart items by session_id
    cart_items = Cart.objects.filter(session_id=session_id)
    cart_total = sum(item.card.price * item.quantity for item in cart_items)

    # Adding total_price to each cart item
    for item in cart_items:
        item.total_price = item.card.price * item.quantity
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})


def card_detail(request, card_id):
    # Fetch the card with the given ID
    card = get_object_or_404(Card, id=card_id)
    
    return render(request, 'card_detail.html', {
        'card': card
    })


def update_cart(request, item_id):
    session_id = request.session.session_key
    if not session_id:
        return redirect('cart')

    # Get the cart item by session_id
    item = get_object_or_404(Cart, id=item_id, session_id=session_id)
    item.quantity = int(request.POST['quantity'])
    
    # Ensure that the new quantity doesn't exceed available stock
    if item.quantity > item.card.inventory:
        item.quantity = item.card.inventory

    item.save()

    return redirect('cart')


def remove_from_cart(request, item_id):
    session_id = request.session.session_key
    if not session_id:
        return redirect('cart')

    # Get the cart item by session_id
    item = get_object_or_404(Cart, id=item_id, session_id=session_id)
    item.delete()

    return redirect('cart')


def contact(request):
    return render(request, 'Contact.html')


def checkout(request):
    session_id = request.session.session_key
    cart_items = Cart.objects.filter(session_id=session_id)

    for item in cart_items:
        card = item.card
        if card.inventory >= item.quantity:
            card.inventory -= item.quantity
            card.save()

    # Clear the cart after purchase
    cart_items.delete()

    return render(request, 'checkout.html')
def checkout_view(request):
    if request.method == "POST":
        # Process the form data here and handle payment integration (Stripe, PayPal)
        return redirect('checkout_success')  # Redirect to success page after payment

    # Example: Get cart from session
    cart = request.session.get('cart', {})
    total = sum(item['product'].price * item['quantity'] for item in cart.values())

    return render(request, 'checkout.html', {'cart': cart, 'total': total})