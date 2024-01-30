from django.urls import path, re_path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('creations/', views.ProductListView.as_view(), name='creations'),
    re_path(r'^creation/(?P<pk>[0-9a-f-]+)$', views.ProductDetailView.as_view(), name='creation-detail'),
]