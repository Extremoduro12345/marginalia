from django.urls import path, re_path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('creations/', views.ProductListView.as_view(), name='creations'),
    path('transmediality/', views.TransmedialityListView.as_view(), name='transmediality'),
    re_path(r'^creation/(?P<pk>[0-9a-f-]+)$', views.product_detail_view, name='creation-detail'),
    re_path(r'^knot/(?P<pk>[0-9a-f-]+)$', views.knot_detail_view, name='knot-detail'),
]
