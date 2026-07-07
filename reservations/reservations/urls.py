from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from catalogue import views as catalogue_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('artist/', include('catalogue.urls')),
    path('register/', catalogue_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='catalogue/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='artist_index'), name='logout'),
]