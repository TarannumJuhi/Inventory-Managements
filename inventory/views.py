from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Supplier, Sale
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models import F

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock_quantity__lte=F('alert_threshold'))
    recent_sales = Sale.objects.order_by('-sale_date')[:5]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category:
        products = products.filter(category__name=category)
    
    if min_price:
        products = products.filter(price__gte=float(min_price))
    
    if max_price:
        products = products.filter(price__lte=float(max_price))

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    categories = Category.objects.all()
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        supplier_id = request.POST.get('supplier')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        alert_threshold = request.POST.get('alert_threshold')
        image = request.FILES.get('image')

        product = Product.objects.create(
            name=name,
            category_id=category_id,
            supplier_id=supplier_id,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            alert_threshold=alert_threshold,
            image=image
        )
        messages.success(request, 'Product created successfully!')
        return redirect('product_detail', pk=product.pk)
    
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/product_form.html', {
        'categories': categories,
        'suppliers': suppliers
    })

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.supplier_id = request.POST.get('supplier')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock_quantity = request.POST.get('stock_quantity')
        product.alert_threshold = request.POST.get('alert_threshold')
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_detail', pk=product.pk)
    
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/product_form.html', {
        'product': product,
        'categories': categories,
        'suppliers': suppliers
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

@login_required
def record_sale(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity <= product.stock_quantity:
            Sale.objects.create(
                product=product,
                quantity=quantity,
                unit_price=product.price,
                sold_by=request.user
            )
            messages.success(request, 'Sale recorded successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Insufficient stock!')
    return render(request, 'inventory/record_sale.html', {'product': product})

@login_required
def export_inventory(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Category', 'Supplier', 'Price', 'Stock Quantity', 'Alert Threshold'])
    
    products = Product.objects.all()
    for product in products:
        writer.writerow([
            product.name,
            product.category.name,
            product.supplier.name if product.supplier else '',
            product.price,
            product.stock_quantity,
            product.alert_threshold
        ])
    
    return response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
