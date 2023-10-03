from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from .models import Board, Comment, List, Card
from .serializers import BoardSerializer, CommentSerializer, ListSerializer, CardSerializer



from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    http_method_names = ['get', 'post', 'put', 'head', 'options', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['POST'])
    def invite_user(self, request, pk=None):
        board = self.get_object()
        user_id = request.data.get('user_id')
        
        if user_id is not None:
        
            board.users.add(user_id)
            board.save()
            
            return Response({"message": "User invited successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User ID is missing in the request"}, status=status.HTTP_400_BAD_REQUEST)


class BoardSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)
    # queryset = Board.objects.all()
    serializer_class = BoardSerializer

    http_method_names = ['get', 'post', 'put', 'head', 'options', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Board.objects.filter(user__id=user_id)
        return queryset


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = List.objects.filter(board__id=category_id)
        return queryset



class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Card.objects.all()

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Card.objects.filter(list__id=category_id)
        return queryset



class CardAllViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Card.objects.all()



class ListAllViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = List.objects.all()



class CreateCommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Card.objects.all()

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Comment.objects.filter(card__id=category_id).order_by("-id")
        return queryset