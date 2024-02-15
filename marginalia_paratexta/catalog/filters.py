import django_filters
from .models import Country,  Genre, KeyWord, Product
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.db import models
from functools import reduce
from operator import or_
from django.db.models import Q

YEAR_CHOICES = [(str(year), str(year)) for year in range(1930, 2025)]

class YearRangeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        year_range = [(year, str(year)) for year in range(1930, 2025)]
        widgets = (
            forms.Select(attrs=attrs, choices=year_range),
            forms.Select(attrs=attrs, choices=year_range),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value
        return [None, None]  


class YearRangeFilter(django_filters.RangeFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', YearRangeWidget())  # Usa nuestro widget personalizado
        super().__init__(*args, **kwargs)
        # Establece el valor predeterminado para el segundo campo del rango a 2024
        self.extra['widget'].widgets[1].choices = [(None, '---------')] + YEAR_CHOICES
        self.extra['widget'].widgets[1].initial = 2024
        self.extra['widget'].widgets[0].choices = [(None, '---------')] + YEAR_CHOICES
        self.extra['widget'].widgets[0].initial = 1930

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Título')

    palabras_clave = django_filters.ModelMultipleChoiceFilter(
        field_name='creation__palabras_clave',
        queryset=KeyWord.objects.all(),
        label='Palabras Clave',
        conjoined=True 
    )
    genero = django_filters.ModelMultipleChoiceFilter(
        field_name='creation__genero',  # Ajusta el campo para reflejar la relación con el género
        queryset=Genre.objects.all(),
        label='Género',
        conjoined=True 
    )

    paises = django_filters.ModelMultipleChoiceFilter(
        field_name='creation__paises', 
        queryset=Country.objects.all(),
        label='Paises Relacionados',
        conjoined=True 
    )
    
    creation_type = django_filters.ChoiceFilter(
        label='Tipo de Creación',
        method='filter_by_creation_type',
        choices=[
            ('movie', 'Movie'),
            ('tvserie', 'TV Serie'),
            ('theatre', 'Theatre'),
            ('musica', 'Musica'),
            ('boardgame', 'Boardgame'),
            ('videogame', 'VideoGame'),
            ('comic', 'Comic'),
            ('novel', 'Novel'),
        ]
    )


    publication_year_range = YearRangeFilter(
        field_name='creation__publication_year',
        label='Rango de años de publicación'
    )

    class Meta:
        model = Product
        fields = ['title', 'palabras_clave', 'genero', 'creation_type', 'publication_year_range', 'paises'  ]


    def filter_by_creation_type(self, queryset, name, value):
        content_type = ContentType.objects.get(model=value)
        return queryset.filter(creation__polymorphic_ctype_id=content_type.id)
