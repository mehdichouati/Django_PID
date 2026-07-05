from django.urls import path
from . import views

urlpatterns = [
    path('', views.artist_index, name='artist_index'),
    path('<int:id>', views.artist_show, name='artist_show'),
]