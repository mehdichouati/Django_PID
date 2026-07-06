from django.urls import path
from . import views

urlpatterns = [
    path('', views.artist_index, name='artist_index'),
    path('create', views.artist_create, name='artist_create'),
    path('store', views.artist_store, name='artist_store'),
    path('edit/<int:id>', views.artist_edit, name='artist_edit'),
    path('update/<int:id>', views.artist_update, name='artist_update'),
    path('delete/<int:id>', views.artist_delete, name='artist_delete'),
    path('<int:id>', views.artist_show, name='artist_show'),
]