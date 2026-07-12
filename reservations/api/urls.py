from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ArtistListCreateView, ArtistRetrieveUpdateDestroyView,
    ShowListCreateView, ShowRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('artists/', ArtistListCreateView.as_view(), name='artist-list'),
    path('artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'),
    path('shows/', ShowListCreateView.as_view(), name='show-list'),
    path('shows/<int:pk>/', ShowRetrieveUpdateDestroyView.as_view(), name='show-detail'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]