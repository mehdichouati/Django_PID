from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_index, name='show_index'),
    path('create', views.show_create, name='show_create'),
    path('store', views.show_store, name='show_store'),
    path('<int:id>', views.show_show, name='show_show'),
]