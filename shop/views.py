from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Category, Order, Profile, OrderEntry
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)


class Registration(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("shop:products_view")
    template_name = "registration/registration.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('shop:products_view')
    else:
        return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return redirect('shop:products_view')


def products_view(request, page_number=1):
    # if page_number > 4:
    #     page_number = 4
    # if page_number < 1:
    #     page_number = 1
    context = Paginator(Product.objects.all().order_by('category'), 2)
    page_obj = context.get_page(page_number)
    return render(request, 'shop/products.html', {'products': page_obj, 'context': context})


def products_detail(request, product_id: int):
    context = {'product': get_object_or_404(Product, id=product_id)}
    return render(request, 'shop/product_detail.html', context)


def categories_view(request):
    context = {'categories': Category.objects.all()}
    return render(request, 'shop/categories.html', context)


def categories_products(request, categories_id: int):
    context = {'category_product': get_object_or_404(Category, id=categories_id)}
    return render(request, 'shop/categories_products.html', context)


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST['id']
        product = get_object_or_404(Product, id=product_id)
        profile = Profile.objects.get_or_create(user=request.user)
        if not profile[0].shopping_cart or profile[0].shopping_cart.status == 'COMPLETED':
            profile[0].shopping_cart = Order.objects.create(profile=profile[0])
            profile[0].save()
        order_entry = OrderEntry.objects.get_or_create(order=profile[0].shopping_cart, product=product)
        order_entry[0].count += 1
        order_entry[0].save()
        return redirect('shop:products_detail', product_id=product_id)
    else:
        profile = Profile.objects.get_or_create(user=request.user)
        if not profile[0].shopping_cart:
            profile[0].shopping_cart = Order.objects.create(profile=profile[0])
            profile[0].save()
        basket = OrderEntry.objects.filter(order=profile[0].shopping_cart, order__status='INITIAL')
        return render(request, 'shop/add_to_cart.html', {'basket': basket, 'price': profile[0].shopping_cart.total_price()})


@login_required
def del_from_cart(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id')
        profile = Profile.objects.get(user=request.user)
        for product_id in product_ids:
            product = get_object_or_404(Product, id=product_id)
            OrderEntry.objects.filter(order=profile.shopping_cart, product=product).delete()
            profile.shopping_cart.save()
        return redirect('shop:add_to_cart')


@login_required
def change_count(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        count = int(request.POST['count'])
        profile = Profile.objects.get(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        if count == 0:
            OrderEntry.objects.filter(order=profile.shopping_cart, product=product).delete()
            profile.shopping_cart.save()
            return redirect('shop:add_to_cart')
        order_entry = OrderEntry.objects.get(order=profile.shopping_cart, product=product)
        order_entry.count = count
        order_entry.save()
        profile.shopping_cart.save()
        return redirect('shop:add_to_cart')


@login_required
def completed_order(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        print(profile.shopping_cart)
        profile.shopping_cart.status = 'COMPLETED'
        profile.shopping_cart.save()
        messages.success(request, 'Your order has been placed!')
        return redirect('shop:add_to_cart')


@login_required
def account_page(request):
    profile = Profile.objects.get(user=request.user)
    completed_orders = Order.objects.filter(status='COMPLETED', profile=profile).order_by('-id')[:5]
    context = {'profile': profile, 'completed_orders': completed_orders}
    return render(request, 'shop/account_page.html', context)


@login_required
def change_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        profile = Profile.objects.get(user=request.user)
        if first_name:
            profile.user.first_name = first_name
            profile.user.save()
        if last_name:
            profile.user.last_name = last_name
            profile.user.save()
        if email:
            profile.user.email = email
            profile.user.save()
        return redirect('shop:account_page')



