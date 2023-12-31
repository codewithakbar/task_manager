from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone


from trello.permissions import IsAdminUser, IsAdminUserOrReadOnly, IsOddiyAdminUser

from users.models import CustomUser, Departaments
from .models import BajarilganBoard, Board, ChekBoard, TugatilmaganBoard, BajarilmaganBoard, Comment, List, Card
from .serializers import (
    BoardSerializer, ChekBoardSerializer, DepartamentsSerializer, TugatilmaganBoardSerializer, BajarilmaganBoardSerializer, CommentSerializer, 
    CommentSerializerPOST, ListSerializer, CardSerializer
)



class TugatilmaganViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAdminUser]
    queryset = TugatilmaganBoard.objects.all()
    serializer_class = TugatilmaganBoardSerializer



class BajarilganBoardViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAdminUser]
    queryset = Board.objects.filter(bajarilgan=True)
    serializer_class = TugatilmaganBoardSerializer



class ChekBoardViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAdminUser]
    queryset = ChekBoard.objects.all()
    serializer_class = ChekBoardSerializer


class DepartamentsViewSet(viewsets.ModelViewSet):
    
    permission_classes = (IsAdminUser,)
    queryset = Departaments.objects.all()
    serializer_class = DepartamentsSerializer


class AddDepUsers(viewsets.ModelViewSet):
    
    permission_classes = (IsAdminUser,)
    queryset = Departaments.objects.all()
    serializer_class = DepartamentsSerializer

    

# Admin metodi

class UserBoardUsers(viewsets.ModelViewSet):

    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    

class AllBardAdminViewSet(viewsets.ModelViewSet):
    """Boardagi hamma objectni oladi"""
    permission_classes = (IsAdminUser,)
    queryset = Board.objects.filter(status_active=True)
    serializer_class = BoardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)

        board_instance = serializer.instance

        user_ids = request.data.get('user', [])
        for user_id in user_ids:
            try:
                user = CustomUser.objects.get(id=user_id)
                board_instance.user.add(user)
            except CustomUser.DoesNotExist:
                return Response({"error": f"User with ID {user_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        board_instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def boar_to_tugatilmagan(self, request, pk):
        try:
            source_instance = Board.objects.get(pk=pk)

            target_instance = TugatilmaganBoard(id=source_instance.id, title=source_instance.title)
            target_instance.save()

            target_instance.user.set(source_instance.user.all())

            # source_instance2 = Board(id=source_instance.id, status_active=False)
            # source_instance2.save()

            source_instance.delete()

            return Response({"message": "Data moved successfully"})
        except Board.DoesNotExist:
            return Response(
                {"error": "SourceModel with the specified ID does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )


    def board_to_bajarilgan(sekf, request, pk):
        try:
            source_inctance = Board.objects.get(pk=pk)
            source_inctance.bajarilgan = True
            source_inctance.status_active = False
            source_inctance.save()
            
            return Response({"message": "Data moved successfully"})

        except Board.DoesNotExist:
            return Response(
                {"error": "SourceModel with the specified ID does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def board_to_bajarilmagan(sekf, request, pk):
        try:
            source_inctance = Board.objects.get(pk=pk)
            source_inctance.bajarilmagan = True
            source_inctance.status_active = False
            source_inctance.save()
            
            return Response({"message": "Data moved successfully"})

        except Board.DoesNotExist:
            return Response(
                {"error": "SourceModel with the specified ID does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['POST'])
    def invite_user(self, request, pk=None):
        board = self.get_object()
        user_id = request.data.get('user_id')
        
        if user_id is not None:
        
            board.user.add(user_id)
            board.save()
            
            return Response({"message": "User invited successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User ID is missing in the request"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['POST'])
    def remove_user_in_board(self, request, pk=None):
        board = self.get_object()
        user_id = request.data.get('user_id')

        if user_id is not None:
            try:
                user_to_remove = CustomUser.objects.get(id=user_id)
                board.user.remove(user_to_remove)
                board.save()
                return Response({"message": "User removed from the board successfully!"}, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User ID is missing in the request"}, status=status.HTTP_400_BAD_REQUEST)











# Userniki 


class UserBoardSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
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






class AllBardUserViewSet(viewsets.ModelViewSet):
    """ Foydalanuvchi boardni bajarishga yuvaradi """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Board.objects.filter(status_active=True)
    serializer_class = BoardSerializer


    def user_to_check_board(self, request, pk):
        try:
            source_instance = Board.objects.get(pk=pk)

            target_instance = ChekBoard(id=source_instance.id, title=source_instance.title)
            target_instance.save()

            target_instance.user.set(source_instance.user.all())

            # source_instance2 = Board(id=source_instance.id, status_active=False)
            # source_instance2.save()

            source_instance.delete()
            
            

            return Response({"message": "Data moved successfully"})
        except Board.DoesNotExist:
            return Response(
                {"error": "SourceModel with the specified ID does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )





# lishniy
class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    http_method_names = ['get', 'post', 'put', 'head', 'options', 'delete']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_time_expired()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_time_expired()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        board_instance = serializer.instance

        if board_instance.is_time_expired():
            board_instance.status_active = False
            board_instance.bajarilmoqda = False
            board_instance.bajarilmagan = True
        else:
            board_instance.status_active = True
            board_instance.bajarilmoqda = True
            board_instance.bajarilmagan = False


        user_ids = request.data.get('user', [])
        for user_id in user_ids:
            try:
                user = CustomUser.objects.get(id=user_id)
                board_instance.user.add(user)
            except CustomUser.DoesNotExist:
                return Response({"error": f"User with ID {user_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        board_instance.save()

        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

    # def get_queryset(self):

    #     user_id = self.kwargs['user_id']

    #     board_instance = self.get_object()
    #     user = CustomUser.objects.get(id=user_id)

    #     board_instance.user.add(user)
    #     board_instance.save()
        
    #     queryset = Board.objects.filter(user__id=user_id).order_by('-id')
    #     return queryset 



class BoardSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
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
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Card.objects.all()

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Comment.objects.filter(card__id=category_id).order_by('-id')
        return queryset


class CommentViewSetPOST(viewsets.ModelViewSet):
    serializer_class = CommentSerializerPOST
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    

class GetBoardToOddiyAdmin(viewsets.ModelViewSet):

    serializer_class = BoardSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Board.objects.filter(user__id=user_id).order_by('-id')
        return queryset


