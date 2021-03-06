from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Product
from .forms import ProductForm, ProductSearchForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.

# Show Products
def show_products(request):
    form = ProductSearchForm()
    all_products = Product.objects.all()
    if request.GET.get('search_by_name'):
        all_products = all_products.filter(name__contains=request.GET.get('search_by_name'))

    if request.GET.get('min_cost'):
        all_products = all_products.filter(price__gte=request.GET.get('min_cost'))
        
    if request.GET.get('max_cost'):
        all_products = all_products.filter(price__lte=request.GET.get('max_cost'))
        
    return render(request, 'catalog/products.template.html', {
        'all_products': all_products,
        'search_form': form
    })


# Create Product
@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Product [" + form.data.get('name') + "] has been added!") 
            return redirect(show_products)
      
    else:
        product_form = ProductForm()
  
    return render(request, 'catalog/create_product.template.html', {
        'form': product_form
    })
    
# Update/Edit Product only for superusers/admin
@user_passes_test(lambda u: u.is_superuser)
def update_product(request, product_id):
    product_updated = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_updated)
        if form.is_valid():
            form.save()
            messages.success(request,"Product [" + form.data.get('name') + "] has been updated!")
            return redirect(reverse(show_products))
            
    else:
        update_form = ProductForm(instance=product_updated)
            
    return render(request, 'catalog/update_product.template.html', {
        'form': update_form
    })
            

# Confirm Product to be deleted only for superusers/admin
@user_passes_test(lambda u: u.is_superuser)
def confirm_delete_product(request, product_id):
    delete_product = get_object_or_404(Product, pk=product_id)
    return render(request, 'catalog/confirm_delete_product.template.html', {
        'product':delete_product
    })
    
# Actually deleting Product only for superusers/admin
@user_passes_test(lambda u: u.is_superuser)
def actually_delete_product(request, product_id):
    product_being_deleted = get_object_or_404(Product, pk=product_id)
    product_being_deleted.delete()
    return redirect(reverse('show_products'))