from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import BoardGame, Comic, Movie, Musica, Novel, Product, MedialTransfers, Theatre, Videogame
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from .forms import SignUpForm

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Procesar el formulario y realizar el registro
            # Ejemplo: Guardar el usuario en la base de datos
            user = form.save()
            
            # Puedes agregar acciones adicionales aquí si es necesario, como enviar un correo de confirmación
            
            return redirect('login')  # Redirigir al inicio de sesión después del registro
        else:
            error_messages = form.errors.values()  # Obtener todos los mensajes de error
            for message in error_messages:
                messages.error(request, message)
            return render(request, 'registration/signup.html', {'form': form})

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_products = Product.objects.all().count()

    context = {
        'num_products': num_products,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@method_decorator(login_required, name='dispatch')
class ProductListView( generic.ListView):
    model = Product
    context_object_name = 'product_list'

@method_decorator(login_required, name='dispatch')
class TransmedialityListView(generic.ListView):
    model = MedialTransfers
    context_object_name = 'transmediality_list'

@method_decorator(login_required, name='dispatch')
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
