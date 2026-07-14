from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from catalogue import views as catalogue_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('artist/', include('catalogue.urls')),
    path('show/', include('catalogue.urls_show')),
    path('api/', include('api.urls')),
    path('profile/', catalogue_views.profile_edit, name='profile_edit'),
    path('register/', catalogue_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='catalogue/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='artist_index'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='catalogue/password_reset_form.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='catalogue/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='catalogue/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='catalogue/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('reservation/create/<int:representation_id>', catalogue_views.reservation_create, name='reservation_create'),
    path('reservation/store/<int:representation_id>', catalogue_views.reservation_store, name='reservation_store'),
    path('my-reservations/', catalogue_views.my_reservations, name='my_reservations'),
]