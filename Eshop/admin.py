from django.contrib import admin
from .models import Product, Client, Employee, ShoppingCart, ProductShoppingcart, Order, OrderProduct
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        if request.user.is_staff:
            return True 
        if request.user.is_superuser:
            return False
        return False
    def has_change_permission(self, request, obj = None):
        if obj is not None and request.user.username == obj.employee.user.username:
            return True 
        return False 
    
    def has_delete_permission(self, request, obj = None):
        if obj is not None and request.user.username == obj.employee.user.username:
            return True 
        return False 
admin.site.register(Product, ProductAdmin)

class ClientAdmin(admin.ModelAdmin):
    exclude = ['shopping_cart']
    def save_model(self, request, obj, form, change):
        shopping_cart = ShoppingCart()
        shopping_cart.save()
        obj.shopping_cart = shopping_cart
        super().save_model(request, obj, form, change)
admin.site.register(Client, ClientAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True 
        return False
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True 
        return False 
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False 
admin.site.register(Employee, EmployeeAdmin)

class ShoppingCartAdmin(admin.ModelAdmin):
    pass 
admin.site.register(ShoppingCart, ShoppingCartAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass 
admin.site.register(Order, OrderAdmin)

class OrderProductAdmin(admin.ModelAdmin):
    pass 
admin.site.register(OrderProduct, OrderProductAdmin)

class ProductCartAdmin(admin.ModelAdmin):
    pass 
admin.site.register(ProductShoppingcart, ProductCartAdmin)