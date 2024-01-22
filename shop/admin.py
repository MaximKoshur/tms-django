from django.contrib import admin
from .models import Category, Product, Profile, OrderEntry, Order
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

admin.site.register(Product)
# admin.site.register(Order)
admin.site.register(OrderEntry)
admin.site.register(Profile)


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


class OrderInline(admin.StackedInline):
    model = Order
    extra = 0


class OrderEntryInline(admin.StackedInline):
    model = OrderEntry
    extra = 0


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    verbose_name_plural = "Profile"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderEntryInline, ProfileInline]



# Define a new User admin




class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
