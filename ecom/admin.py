from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from.models import Category,Customer,Product,Order,User,Cart

# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    filter_horizontal = ('groups',)  

admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

