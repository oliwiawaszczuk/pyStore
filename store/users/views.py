from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserForm
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from products.models import Product
from purchases.models import Purchase
import math


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Tworzenie użytkownika, ale jeszcze nie zapisywanie go
            # user.password = make_password(form.cleaned_data['password'])  # Haszowanie hasła
            user.save()  # Teraz zapisujemy użytkownika w bazie danych
            return redirect('/login_page')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    products = Product.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None and user.password == password:
            shopping_items = Purchase.objects.filter(username=user)
            total_cost = 0
            for item in shopping_items:
                total_cost += item.product.price
            total_cost = round(total_cost, 1)

            context = {
                'username': username,
                'shopping_items': shopping_items,
                'total_cost': total_cost,
            }

            return render(request, 'main.html', context)
        else:
            context = {'error_message': 'Nieprawidłowe dane logowania.'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def main(request, username, shopping_items, total_cost):
    context = {
        'username': username,
        'shopping_items': shopping_items,
        'total_cost': total_cost,
    }
    return render(request, 'main.html', context)
