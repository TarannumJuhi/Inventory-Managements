from django.contrib import admin
from .models import Product, Category, Supplier, Sale

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone')
    search_fields = ('name', 'contact_person', 'email')
    list_filter = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'price', 'stock_quantity', 'alert_threshold')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity', 'alert_threshold')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'unit_price', 'total_price', 'sale_date', 'sold_by')
    list_filter = ('sale_date', 'sold_by')
    search_fields = ('product__name',)
    date_hierarchy = 'sale_date'
