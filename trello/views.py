from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from .models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer

from rest_framework.authentication import SessionAuthentication


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = List.objects.filter(board__id=category_id)
        return queryset



class CardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Card.objects.all()
    serializer_class = CardSerializer


