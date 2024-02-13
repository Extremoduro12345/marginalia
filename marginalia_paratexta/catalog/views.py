from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from catalog.filters import ProductFilter
from .models import BoardGame, Comic, Country, Creation, Genre, Knot, Movie, Musica, Novel, Product, Theatre, Videogame
from django.contrib import messages
from .forms import SignUpForm
import plotly.graph_objs as go

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

def grafico_barras_view(request):
    genero = request.GET.get('genero')
    
    # Filtrar creaciones por género si se proporciona
    if genero:
        creaciones = Creation.objects.filter(genero__name=genero)
        titulo = f'Número de Creaciones con Género {genero} por Década'
    else:
        creaciones = Creation.objects.all()
        titulo = 'Número de Creaciones por Década'
    # Lógica para generar el gráfico de barras
    # Por ejemplo, contar el número de creaciones por década
    decadas = range(1930, 2040, 10)
    num_creaciones_por_decada = [creaciones.filter(publication_year__range=(decada, decada + 9)).count() for decada in decadas]

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))  # Tamaño del gráfico
    plt.bar(decadas, num_creaciones_por_decada, width=5, align='center')  # Ancho de las barras y alineación
    plt.xticks(decadas) 
    plt.xlabel('Década')
    plt.ylabel('Número de Creaciones')
    plt.title(titulo)

    plt.yticks(range(max(num_creaciones_por_decada) + 1))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))

    # Convertir el gráfico a una imagen base64 para mostrar en el template
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Lista de géneros para mostrar en el formulario de filtrado
    lista_de_generos = Creation.objects.values_list('genero__name', flat=True).distinct().exclude(genero__name=None)
    print(num_creaciones_por_decada)
    # Retorna el contexto con los datos del gráfico y la lista de géneros
    return render(request, 'catalog/graph.html', {'imagen_base64': imagen_base64, 'lista_de_generos': lista_de_generos})

def world_map_view(request):
    creations = Creation.objects.all()

    # Contar el número de creaciones por país
    country_creations_count = {}
    for creation in creations:
        for country in creation.paises.all():
            country_iso = country.iso_code 
            if country_iso not in country_creations_count:
                country_creations_count[country_iso] = 1
            else:
                country_creations_count[country_iso] += 1

    # Crear los datos del mapa
    data = [go.Choropleth(
        locations=list(country_creations_count.keys()),
        z=list(country_creations_count.values()),
        locationmode='ISO-3',
        colorscale='Viridis',
        marker_line_color='black',
        marker_line_width=0.5,
    )]

    # Crear el diseño del mapa
    layout = go.Layout(
        title='Número de Creaciones por País',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        width=1000,  # Ancho del mapa en píxeles
        height=600,  # Alto del mapa en píxeles
    )

    # Crear la figura del mapa
    fig = go.Figure(data=data, layout=layout)

    # Convertir la figura a JSON para enviarla a la plantilla
    graph_json = fig.to_json()

    return render(request, 'catalog/map.html', {'graph_json': graph_json})
