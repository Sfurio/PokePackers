from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import Card,Cart
from django.shortcuts import render, get_object_or_404  # Ensure this is at the top



# Create your views here.
def home(request):
    images = ['sampic.JPG', 'marisite.JPG', 'WebExCode.JPG']
    return render(request, 'home.html', {'images': images})

def regular_cards(request):
    sort_by = request.GET.get('sort', 'name')  # Default sorting by name
    
    # Validate sort_by to ensure it's a valid field
    valid_sort_fields = ['name', 'price', 'set']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'  # Default to 'name' if invalid sort field

    cards = Card.objects.filter(type='Regular').order_by(sort_by)

    paginator = Paginator(cards, 24)  # Show 24 cards per page (update comment if needed)
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
        cards = Card.objects.filter(type='Reverse').order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='Reverse').order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='Reverse').order_by('name')
    else:
        cards = Card.objects.filter(type='Reverse')

    # Pagination (if needed)
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Reverse.html', {
        'cards': page_obj,
        'is_paginated': True if paginator.num_pages > 1 else False,
        'page_obj': page_obj,
    })

def foil_cards(request):
    sort_option = request.GET.get('sort')
    
    if sort_option == 'price':
        cards = Card.objects.filter(type='Foil').order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='Foil').order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='Foil').order_by('name')
    else:
        cards = Card.objects.filter(type='Foil')

    # Pagination (if needed)
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Foil.html', {
        'cards': page_obj,
        'is_paginated': True if paginator.num_pages > 1 else False,
        'page_obj': page_obj,
    })

def rare_cards(request):
    sort_option = request.GET.get('sort')
    
    if sort_option == 'price':
        cards = Card.objects.filter(type='Rare').order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='Rare').order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='Rare').order_by('name')
    else:
        cards = Card.objects.filter(type='Rare')

    # Pagination (if needed)
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Rare.html', {
        'cards': page_obj,
        'is_paginated': True if paginator.num_pages > 1 else False,
        'page_obj': page_obj,
    })
def PSA_Graded(request):
    sort_option = request.GET.get('sort')
    
    if sort_option == 'price':
        cards = Card.objects.filter(type='PSA').order_by('price')
    elif sort_option == 'series':
        cards = Card.objects.filter(type='PSA').order_by('set')
    elif sort_option == 'name':
        cards = Card.objects.filter(type='PSA').order_by('name')
    elif sort_option == 'grade':
        cards = Card.objects.filter(type='PSA').order_by('grade')
    else:
        cards = Card.objects.filter(type='PSA')

    # Pagination (if needed)
    paginator = Paginator(cards, 10)  # Show 10 cards per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Psa.html', {
        'cards': page_obj,
        'is_paginated': True if paginator.num_pages > 1 else False,
        'page_obj': page_obj,
    })

def add_to_cart(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    
    # Ensure session key exists
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key

    # Try to get the Cart item; if not found, create one with quantity = 1
    cart, created = Cart.objects.get_or_create(session_id=session_id, card=card, defaults={'quantity': 1})

    if not created:
        # If the Cart item already exists, increase the quantity
        cart.quantity += 1
        cart.save()
    
    return redirect('cart')  # Redirect to a cart page or similar

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'cart.html', context)


def card_detail(request, card_id):
    # Fetch the card with the given ID
    card = get_object_or_404(Card, id=card_id)
    
    return render(request, 'card_detail.html', {
        'card': card
    })


def update_cart(request, item_id):
    item = Cart.objects.get(id=item_id, user=request.user)
    item.quantity = int(request.POST['quantity'])
    item.save()
    return redirect('cart')

def remove_from_cart(request, item_id):
    item = Cart.objects.get(id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

def contact(request):
    return render(request, 'Contact.html')