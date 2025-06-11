# views.py
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib import messages
from django.db.models import F
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required





def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('products')  
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    total_categories = Category.objects.count()
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(stock__lte=F('stock_min')).count()


    if request.method == "POST":
        name = request.POST.get("name").strip()
        category_id = request.POST.get("category")
        supplier_id = request.POST.get("supplier")
        stock_min = int(request.POST.get("stock_min", 0))
        stock = int(request.POST.get("stock", 0))
        image = request.FILES.get("image")

        # Get related objects
        category = Category.objects.get(id=category_id)
        supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None

        # Check for existing product with same name and category
        if Product.objects.filter(name__iexact=name, category=category).exists():
            messages.warning(request, "Product already exists.")
        else:
            Product.objects.create(
                name=name,
                category=category,
                supplier=supplier,
                stock_min=stock_min,
                stock=stock,
                image=image,
            )
            messages.success(request, "Product added successfully.")

        return redirect(request.path)  # Reload to show message

    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'suppliers': suppliers,
        'total_categories' : total_categories,
        'total_products' : total_products,
        'low_stock_count' : low_stock_count,
    })

@login_required
def suppliers(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        Supplier.objects.create(name=name, contact=contact)
        return redirect(request.path)  # Refreshes same page
    suppliers = Supplier.objects.all()
    return render(request, "supplier.html", {"suppliers": suppliers})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def categories(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()

        if Category.objects.filter(name__iexact=name).exists():
            messages.warning(request, "The category already exists.")
        else:
            Category.objects.create(name=name)
            messages.success(request, "Category created successfully.")

        return redirect(request.path)  # Refresh same page to show messages

    categories = Category.objects.all()
    return render(request, "category.html", {"categories": categories})


@login_required
def stock_in(request):
    products = Product.objects.all()
    stockins = StockIn.objects.all().order_by('-date')

    if request.method == "POST":
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        note = request.POST.get('note', '')

        # Validate inputs
        if not product_id or not quantity:
            messages.error(request, "Product and quantity are required.")
            return redirect(request.path)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                messages.error(request, "Quantity must be positive.")
                return redirect(request.path)
        except ValueError:
            messages.error(request, "Quantity must be a number.")
            return redirect(request.path)

        product = get_object_or_404(Product, id=product_id)

        # Create StockIn record
        StockIn.objects.create(
            product=product,
            quantity=quantity,
            note=note
        )

        # Update product stock
        product.stock += quantity
        product.save()

        messages.success(request, f"Added {quantity} units to '{product.name}'. Stock updated.")
        return redirect(request.path)

    return render(request, 'stock_in.html', {
        'stockins': stockins,
        'products' : products,
    })

@login_required
def stock_out(request):
    products = Product.objects.all()
    stockouts = StockOut.objects.select_related('product').all().order_by('-date')

    if request.method == "POST":
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        note = request.POST.get('note', '')

        # Validate inputs
        if not product_id or not quantity:
            messages.error(request, "Product and quantity are required.")
            return redirect(request.path)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                messages.error(request, "Quantity must be positive.")
                return redirect(request.path)
        except ValueError:
            messages.error(request, "Quantity must be a number.")
            return redirect(request.path)

        product = get_object_or_404(Product, id=product_id)

        if quantity > product.stock:
            messages.error(request, f"Cannot remove {quantity} units. Only {product.stock} units in stock.")
            return redirect(request.path)

        # Create StockOut record
        StockOut.objects.create(
            product=product,
            quantity=quantity,
            note=note
        )

        # Update product stock
        product.stock -= quantity
        product.save()

        messages.success(request, f"Removed {quantity} units from '{product.name}'. Stock updated.")
        return redirect(request.path)

    return render(request, 'stock_out.html', {
        'stockouts': stockouts,
        'products': products,
    })


def logout_view(request):
    logout(request)
    return redirect('login')