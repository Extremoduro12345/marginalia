from django.shortcuts import render
from django.views import generic
from .models import BoardGame, Comic, Movie, Musica, Novel, Product, MedialTransfers, Theatre, Videogame
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

class TransmedialityListView(generic.ListView):
    model = MedialTransfers
    context_object_name = 'transmediality_list'

class ProductDetailView(generic.DetailView):
    model = Product

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if isinstance(product.creation, Movie):    
        context = {
            'product': product,
            'type': "Película"
        }
    elif isinstance(product.creation, Videogame):    
        context = {
            'product': product,
            'type': "Videojuego"
        } 
    elif isinstance(product.creation, Musica):    
        context = {
            'product': product,
            'type': "Música"
        } 
    elif isinstance(product.creation, BoardGame):    
        context = {
            'product': product,
            'type': "Juego de mesa"
        } 
    elif isinstance(product.creation, Comic):    
        context = {
            'product': product,
            'type': "Comic"
        } 
    elif isinstance(product.creation, Novel):    
        context = {
            'product': product,
            'type': "Novela"
        }
    elif isinstance(product.creation, Theatre):    
        context = {
            'product': product,
            'type': "Teatro"
        }  
    else :
        context = {
            'product': product,
            'type': "Serie de television"
        }
    return render(request, 'catalog/product_detail.html', context=context)
