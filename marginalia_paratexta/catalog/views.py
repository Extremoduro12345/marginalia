from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View

from catalog.filters import ProductFilter
from .models import BoardGame, Comic, Knot, Movie, Musica, Novel, Product, Theatre, Videogame
from django.urls import reverse_lazy
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

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_products = Product.objects.all().count()

    context = {
        'num_products': num_products,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class ProductListView( generic.ListView):
    model = Product
    context_object_name = 'product_list'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class KnotListView(generic.ListView):
    model = Knot
    context_object_name = 'knot_list'

class ProductDetailView(generic.DetailView):
    model = Product

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user_belongs_to_group = request.user.groups.filter(name='Marginalia Member').exists()

    if isinstance(product.creation, Movie):    
        context = {
            'product': product,
            'type': "Película",
            'user_belongs_to_group': user_belongs_to_group
        }
    elif isinstance(product.creation, Videogame):    
        context = {
            'product': product,
            'type': "Videojuego",
            'user_belongs_to_group': user_belongs_to_group
        } 
    elif isinstance(product.creation, Musica):    
        context = {
            'product': product,
            'type': "Música",
            'user_belongs_to_group': user_belongs_to_group
        } 
    elif isinstance(product.creation, BoardGame):    
        context = {
            'product': product,
            'type': "Juego de mesa",
            'user_belongs_to_group': user_belongs_to_group
        } 
    elif isinstance(product.creation, Comic):    
        context = {
            'product': product,
            'type': "Comic",
            'user_belongs_to_group': user_belongs_to_group
        } 
    elif isinstance(product.creation, Novel):    
        context = {
            'product': product,
            'type': "Novela",
            'user_belongs_to_group': user_belongs_to_group
        }
    elif isinstance(product.creation, Theatre):    
        context = {
            'product': product,
            'type': "Teatro",
            'user_belongs_to_group': user_belongs_to_group
        }  
    else :
        context = {
            'product': product,
            'type': "Serie de television",
            'user_belongs_to_group': user_belongs_to_group
        }
    return render(request, 'catalog/product_detail.html', context=context)

def knot_detail_view(request, pk):
    knot = get_object_or_404(Knot, pk=pk)

    context = {
        'knot': knot,
    }

    return render(request, 'catalog/knot_detail.html', context=context)
