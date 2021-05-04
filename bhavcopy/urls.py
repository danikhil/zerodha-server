from django.urls import path

from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('search-name', views.search_name, name='search_name'),
   path('search', views.search, name='search')
]