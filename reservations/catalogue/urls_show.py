from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_index, name='show_index'),
    path('create', views.show_create, name='show_create'),
    path('store', views.show_store, name='show_store'),
    path('export/csv', views.show_export_csv, name='show_export_csv'),
    path('external/venues', views.external_venues, name='external_venues'),
    path('<int:id>/toggle-bookable', views.show_toggle_bookable, name='show_toggle_bookable'),
    path('<int:id>/review', views.review_store, name='review_store'),
    path('<int:id>', views.show_show, name='show_show'),
]