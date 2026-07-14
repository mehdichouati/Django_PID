from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_index, name='show_index'),
    path('create', views.show_create, name='show_create'),
    path('store', views.show_store, name='show_store'),
    path('export/csv', views.show_export_csv, name='show_export_csv'),
    path('import/csv', views.show_import_csv, name='show_import_csv'),
    path('bulk-delete', views.show_bulk_delete, name='show_bulk_delete'),
    path('external/venues', views.external_venues, name='external_venues'),
    path('external/venues/sync', views.sync_locations_from_opendata, name='sync_locations'),
    path('<int:id>/toggle-bookable', views.show_toggle_bookable, name='show_toggle_bookable'),
    path('<int:id>/review', views.review_store, name='review_store'),
    path('<int:id>', views.show_show, name='show_show'),
]