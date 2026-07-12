from rest_framework import generics
from catalogue.models import Artist, Show
from .serializers import ArtistSerializer, ShowSerializer


class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ShowListCreateView(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class ShowRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer