from rest_framework import generics, permissions
from catalogue.models import Artist, Show
from .serializers import ArtistSerializer, ShowSerializer
from .permissions import AffiliateLevelPermission


class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated, AffiliateLevelPermission]


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated, AffiliateLevelPermission]


class ShowListCreateView(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [permissions.IsAuthenticated, AffiliateLevelPermission]


class ShowRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [permissions.IsAuthenticated, AffiliateLevelPermission]