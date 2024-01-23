from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.products_view, name='products_view'),
    path('orders_history', views.orders_history, name='orders_history'),
    path('change_profile', views.change_profile, name='change_profile'),
    path('account_page', views.account_page, name='account_page'),
    path('completed_order', views.completed_order, name='completed_order'),
    path('change_count', views.change_count, name='change_count'),
    path('del_from_cart', views.del_from_cart, name='del_from_cart'),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
    path('account/registration', views.Registration.as_view(), name="registration"),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('products/page=<int:page_number>', views.products_view, name='products_view'),
    path('products/<int:product_id>', views.products_detail, name='products_detail'),
    path('categories', views.categories_view, name='categories_view'),
    path('categories/<int:categories_id>', views.categories_products, name='categories_products'),
]
