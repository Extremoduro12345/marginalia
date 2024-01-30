from django.shortcuts import render
from django.views import generic
from .models import Product
from django.shortcuts import get_object_or_404

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_products = Product.objects.all().count()

    context = {
        'num_products': num_products,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'product_list'


class ProductDetailView(generic.DetailView):
    model = Product

def product_detail_view(request, primary_key):
    product = get_object_or_404(Product, pk=primary_key)
    print("Antes de asignar HOLA")
    studies_tradition_classical_reception = "HOLA"
    if product.product_bibliography:
        bibliography_instance = product.product_bibliography
        studies_tradition_classical_reception = bibliography_instance.studies_tradition_classical_reception
    print("Después de asignar HOLA")

    context = {
        'product': product,
        'studies_tradition_classical_reception': studies_tradition_classical_reception,
        'hola':'hola'
        # Agrega más campos según sea necesario
    }

    return render(request, 'catalog/product_detail.html', context=context)
