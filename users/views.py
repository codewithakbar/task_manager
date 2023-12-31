from rest_framework import generics,status,views,permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action




from .permissions import IsNotStaffUser
from users.models import CustomUser, Notification
from .serializers import CustomUserForAdminSerializer, CustomUserProfileSerializer, CustomUserSerializer, NotificationSerializer, RegisterSerializer,LoginSerializer,LogoutSerializer


from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from trello.permissions import IsAdminUser, IsAdminUserOrReadOnly, IsOddiyAdminUser


from knox.views import LoginView as KnoxLoginView


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Card.objects.all()

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = CustomUser.objects.filter(id=category_id)
        return queryset


class UserToAdminViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return CustomUser.objects.filter(id=user_id)

    @action(detail=True, methods=['PUT'])
    def user_to_admin(self, request, pk=None):
        instance = self.get_object()
        
        user_id = pk

        if user_id is not None:
            request.data['oddiy_admin'] = True

            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        else:
            return Response({"message": "User ID is missing in the request"}, status=status.HTTP_400_BAD_REQUEST)



class CustomUserDetail(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserForAdminSerializer
    lookup_field = 'username'



class UserProfileDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = CustomUserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        queryset = CustomUser.objects.filter(id=user_id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)




class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)



class LoginView(ObtainAuthToken):

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        is_admin = user.is_staff
        oddiy_admin = user.oddiy_admin
        
        profile_image_url = user.profile_image.url if user.profile_image else None
        if profile_image_url:
            profile_image_url = request.build_absolute_uri(profile_image_url)

        return Response(
            {
                'token': token.key, 
                'is_admin': is_admin,
                'oddiy_admin': oddiy_admin,
                'user_id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'photo': profile_image_url,  
            }
        )


        

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    @require_POST
    def post(self, request):
        # Logout the user
        logout(request)
        return JsonResponse({'message': 'Logout successful'})



class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 



class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.all().order_by('-created_at')



class MarkNotificationAsReadView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user, is_read=False)

    def perform_update(self, serializer):
        serializer.save(is_read=True)



class CustomUserListCreateView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return CustomUser.objects.filter(is_staff=False)



class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return CustomUser.objects.filter(is_staff=False)

