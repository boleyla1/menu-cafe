# cafe_app/views.py
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, CafeSettings
from .forms import CategoryForm, ProductForm, CafeSettingsForm
from accounts.forms import RegisterForm,LogimForm,ProfileUpdateForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # ورود به داشبورد فقط برای کاربران وارد شده


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    cafe_settings = CafeSettings.objects.first()  # فرض می‌کنیم فقط یک رکورد از تنظیمات کافه وجود دارد

    if cafe_settings:
        name_parts = cafe_settings.name.split()
        if len(name_parts) > 1:
            cafe_name = {'part1': name_parts[0], 'part2': name_parts[1]}
        else:
            cafe_name = {'part1': cafe_settings.name, 'part2': ''}
    else:
        cafe_name = {'part1': 'کافه', 'part2': 'تالس'}

    return render(request, 'cafe_app/index.html',
                  {'categories': categories, 'products': products, 'cafe_settings': cafe_settings,
                   'cafe_name': cafe_name})


@login_required
def categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'cafe_app/categories.html', {'form': CategoryForm, 'categories': categories})


@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'cafe_app/categories.html', {'categories': Category.objects.all()})


@login_required
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'cafe_app/edit_category.html', {'form': form, 'category': category})


@login_required
def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()

    return render(request, 'cafe_app/products.html', {'products': products, 'form': form, 'categories': categories})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'cafe_app/products.html', {'products': Product.objects.all(), 'form': ProductForm()})


@login_required
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    categories = Category.objects.all()
    return render(request, 'cafe_app/edit_products.html', {'form': form, 'product': product, 'categories': categories})


@login_required
def dashboard_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    cafe_settings = CafeSettings.objects.first()

    return render(request, 'cafe_app/dashboard.html',
                  {'categories': categories, 'products': products, 'cafe_settings': cafe_settings})


@login_required
def settings_view(request):
    CAFE_SETTINGS_ID = 1  # ID ثابت تنظیمات کافه

    cafe_settings = get_object_or_404(CafeSettings, id=CAFE_SETTINGS_ID)

    if request.method == 'POST':
        form = CafeSettingsForm(request.POST, instance=cafe_settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CafeSettingsForm(instance=cafe_settings)

    return render(request, 'cafe_app/setting.html', {'form': form, 'error': form.errors})


def product_list_view(request):
    query = request.GET.get('query')
    products = Product.objects.all()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(category__name__icontains=query)
        )

    product_list = list(products.values('id', 'name', 'price', 'ingredients', 'category__name'))
    return JsonResponse({'results': product_list})



