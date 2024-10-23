from django.shortcuts import render, redirect
from .forms import PurchaseForm
from .models import Purchase, Product
from users.models import User
from django.urls import reverse
import math


def create_purchase(request, product_id, username):
    product = Product.objects.get(name=product_id)
    user = User.objects.get(username=username)

    # Sprawdź, czy istnieje już ten produkt w koszyku
    existing_purchase = Purchase.objects.filter(username=user, product=product).first()

    if existing_purchase:
        # Produkt już istnieje w koszyku, zaktualizuj liczbę
        existing_purchase.count += 1
        existing_purchase.save()
    else:
        # Produkt nie istnieje, stwórz nowy rekord
        purchase = Purchase(username=user, product=product)
        purchase.save()

    # Oblicz nową sumę (total_cost) na podstawie count
    shopping_items = Purchase.objects.filter(username=user)
    total_cost = sum(item.product.price * item.count for item in shopping_items)
    total_cost = round(total_cost, 1)

    context = {
        'username': username,
        'shopping_items': shopping_items,
        'total_cost': total_cost,
    }

    return render(request, 'main.html', context)


# W funkcji main nie musisz już przekazywać shopping_items i total_cost jako argumenty, ponieważ są teraz dostępne w kontekście.
def main(request, username):
    return render(request, 'main.html', {'username': username})

def remove_product(request, username, product_id):
    # Znajdź zakup użytkownika
    user = User.objects.get(username=username)
    product = Product.objects.get(id=product_id)

    try:
        purchase = Purchase.objects.get(username=user, product=product)
    except Purchase.DoesNotExist:
        # Jeśli nie istnieje taki zakup, zrób coś odpowiedniego, np. pokaż komunikat użytkownikowi
        # Tutaj możesz także przekierować użytkownika na stronę z błędem.
        return render(request, 'error.html', {'message': 'Ten produkt nie istnieje w Twoim koszyku.'})

    # Sprawdź, czy liczba produktów (count) w zakupie jest większa niż 1
    if purchase.count > 1:
        # Jeśli tak, zmniejsz tylko liczbę produktów
        purchase.count -= 1
        purchase.save()
    else:
        # W przeciwnym razie (jeśli count wynosi 1), usuń cały rekord Purchase
        purchase.delete()

    # Oblicz ponownie shopping_items i total_cost
    shopping_items = Purchase.objects.filter(username=user)
    total_cost = sum(item.product.price * item.count for item in shopping_items)
    total_cost = round(total_cost, 1)

    context = {
        'username': username,
        'shopping_items': shopping_items,
        'total_cost': total_cost,
    }

    return render(request, 'main.html', context)
