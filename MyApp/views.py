from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Card, Cart, Order, OrderItem
from django.contrib import messages


from django.core.mail import send_mail

import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.method == 'POST':
        # Get cart details
        cart = request.session.get('cart', {})
        total = sum(item['product'].price * item['quantity'] for item in cart.values())

        # Create a Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'PokePackers Order',
                    },
                    'unit_amount': int(total * 100),  # Convert dollars to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/checkout_success/'),
            cancel_url=request.build_absolute_uri('/checkout/'),
        )

        return JsonResponse({'id': session.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

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
    sort_option = request.GET.get('sort')
    series_filter = request.GET.get('series')

    cards = Card.objects.filter(type='Regular', inventory__gt=0)

    if series_filter:
        cards = cards.filter(series=series_filter)

    if sort_option == 'price':
        cards = cards.order_by('price')
    elif sort_option == 'series':
        cards = cards.order_by('series')
    elif sort_option == 'name':
        cards = cards.order_by('name')

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
    series_filter = request.GET.get('series')

    # Base query for reverse cards with inventory greater than 0
    cards = Card.objects.filter(type='Reverse', inventory__gt=0)

    # Filter by series if selected
    if series_filter:
        cards = cards.filter(series=series_filter)

    # Sorting
    if sort_option == 'price':
        cards = cards.order_by('price')
    elif sort_option == 'series':
        cards = cards.order_by('series')
    elif sort_option == 'name':
        cards = cards.order_by('name')

    # Pagination
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all distinct series to display in the dropdown
    all_series = Card.objects.filter(type='Reverse').values_list('series', flat=True).distinct()

    return render(request, 'Reverse.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'all_series': all_series,  # Pass distinct series to template
        'selected_series': series_filter  # Pass selected series to maintain state
    })


def foil_cards(request):
    sort_option = request.GET.get('sort')
    series_filter = request.GET.get('series')

    cards = Card.objects.filter(type='Foil', inventory__gt=0)

    if series_filter:
        cards = cards.filter(series=series_filter)

    if sort_option == 'price':
        cards = cards.order_by('price')
    elif sort_option == 'series':
        cards = cards.order_by('series')
    elif sort_option == 'name':
        cards = cards.order_by('name')

    paginator = Paginator(cards, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_series = Card.objects.filter(type='Foil').values_list('series', flat=True).distinct()

    return render(request, 'Foil.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'all_series': all_series,
        'selected_series': series_filter
    })


def rare_cards(request):
    sort_option = request.GET.get('sort')
    series_filter = request.GET.get('series')

    # Query to get the available series for filtering
    series_list = Card.objects.filter(type='Rare', inventory__gt=0).values_list('series', flat=True).distinct()

    # Base query to get rare cards in stock
    cards = Card.objects.filter(type='Rare', inventory__gt=0)

    # Apply series filter if selected
    if series_filter:
        cards = cards.filter(series=series_filter)

    # Apply sorting based on the selected option
    if sort_option == 'price':
        cards = cards.order_by('price')
    elif sort_option == 'series':
        cards = cards.order_by('series')
    elif sort_option == 'name':
        cards = cards.order_by('name')

    # Pagination
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Rare.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'series_list': series_list,  # Pass the available series to the template
        'selected_series': series_filter,  # Keep track of selected series
    })


def PSA_Graded(request):
    sort_option = request.GET.get('sort')
    series_filter = request.GET.get('series')
    grade_filter = request.GET.get('grade')

    # Query to get the available series and grades for dropdown filters
    series_list = Card.objects.filter(type='PSA', inventory__gt=0).values_list('series', flat=True).distinct()
    grade_list = Card.objects.filter(type='PSA', inventory__gt=0).values_list('grade', flat=True).distinct()

    # Filter cards by type 'PSA' and inventory
    cards = Card.objects.filter(type='PSA', inventory__gt=0)

    # Apply series filter if selected
    if series_filter:
        cards = cards.filter(series=series_filter)

    # Apply grade filter if selected
    if grade_filter:
        cards = cards.filter(grade=grade_filter)

    # Apply sorting based on the selected option
    if sort_option == 'price':
        cards = cards.order_by('price')
    elif sort_option == 'series':
        cards = cards.order_by('series')
    elif sort_option == 'name':
        cards = cards.order_by('name')
    elif sort_option == 'grade':
        cards = cards.order_by('grade')

    # Pagination
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Psa.html', {
        'cards': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'series_list': series_list,  # Pass the series list to the template
        'grade_list': grade_list,    # Pass the grade list to the template
        'selected_series': series_filter,  # Track the selected series
        'selected_grade': grade_filter,    # Track the selected grade
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
    # Ensure session exists
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Get cart items for the current session
    cart_items = Cart.objects.filter(session_id=session_id)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # Calculate the total price for the order
    total = sum(item.card.price * item.quantity for item in cart_items)

    if request.method == "POST":
        stripe_token = request.POST.get('stripeToken')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        if not stripe_token or not full_name or not address or not email:
            messages.error(request, "All fields are required.")
            return render(request, 'checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
            })

        # Create a Stripe charge
        try:
            charge = stripe.Charge.create(
                amount=int(total * 100),  # Stripe accepts the amount in cents
                currency="usd",
                source=stripe_token,
                description="PokePackers Order"
            )

            # Create the order in the database
            order = Order.objects.create(
                full_name=full_name,
                address=address,
                email=email,
                total_price=total
            )

            # Create the order items and adjust inventory
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.card, quantity=item.quantity)

                # Update the inventory
                if item.card.inventory >= item.quantity:
                    item.card.inventory -= item.quantity
                    item.card.save()
                else:
                    messages.error(request, f"Sorry, not enough stock for {item.card.name}.")
                    return render(request, 'checkout.html', {
                        'cart_items': cart_items,
                        'total': total,
                        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
                    })

            # Clear the cart after successful purchase
            cart_items.delete()

            # Redirect to success page
            return redirect('checkout_success')

        except stripe.error.CardError as e:
            messages.error(request, "Your card was declined.")
        except stripe.error.StripeError as e:
            messages.error(request, "There was an error processing your payment. Please try again.")
        except Exception as e:
            messages.error(request, "An unexpected error occurred. Please try again.")

    # Render the checkout page with cart items and total
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY  # Pass Stripe publishable key
    })