
from rest_framework import viewsets, permissions
from .models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer



class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class ListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    queryset = List.objects.all()
    serializer_class = ListSerializer


class CardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Card.objects.all()
    serializer_class = CardSerializer


