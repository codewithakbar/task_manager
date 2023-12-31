"""
URL configuration for asana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns

from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from trello.views import AllBardAdminViewSet, AllBardUserViewSet, BajarilganBoardViewSet, BoardSessionViewSet, BoardViewSet, CardViewSet, ChekBoardViewSet, CommentViewSet, CommentViewSetPOST, CreateCommentView, DepartamentsViewSet, GetBoardToOddiyAdmin, ListViewSet, ListAllViewSet, CardAllViewSet, TugatilmaganViewSet, UserBoardSessionViewSet, UserBoardUsers

from users.views import CustomUserDetail, CustomUserDetailView, CustomUserListCreateView, MarkNotificationAsReadView, NotificationListView, RegisterView, LoginView, LogoutAPIView, UserProfileDetailView, UserProfileViewSet, UserToAdminViewSet
from rest_framework.authtoken.views import obtain_auth_token



router = routers.DefaultRouter()
# router.register(r'register', RegistrationAPIView, basename='register')
# router.register(r'login', LoginAPIView, basename='login')
router.register(r'boards', BoardViewSet)
router.register(r'boards', UserBoardUsers)

# router.register(r'users', CustomUserListCreateView, basename='user-list')
# router.register(r'users/(?P<category_id>\d+)', CustomUserDetailView, basename='user-detail')

router.register(r'all/boards', AllBardAdminViewSet, basename='admin_all_board')
router.register(r'all/departaments', DepartamentsViewSet, basename='admin_all_departaments')
router.register(r'all/tugatilmagan', TugatilmaganViewSet, basename='admin_all_tugatilmagan_board')
router.register(r'all/bajarilgan', BajarilganBoardViewSet, basename='admin_all_bajarilgan_board')
router.register(r'all/chek', ChekBoardViewSet, basename='chek')


router.register(r'get/to/oddiyadmin/(?P<user_id>\d+)', GetBoardToOddiyAdmin, basename='get_to_admin')


router.register(r'list', ListAllViewSet, basename='list_all_board')
router.register(r'comment', CreateCommentView, basename='create_up_del-comment')
router.register(r'comments/card/(?P<category_id>\d+)', CommentViewSet, basename='cardd_by_commnt')
router.register(r'comments/card/post/(?P<category_id>\d+)', CommentViewSetPOST, basename='card_post__dby_commnt')
router.register(r'comment/post/', CommentViewSetPOST, basename='card_post__dby_commnt')

router.register(r'card', CardAllViewSet, basename='card_all_list')
router.register(r'lists/(?P<category_id>\d+)', ListViewSet, basename='texnika')
router.register(r'cards/(?P<category_id>\d+)', CardViewSet, basename='cardd')

router.register(r'userprofile/(?P<category_id>\d+)', UserProfileViewSet, basename='userprofile')
router.register(r'user/boards/(?P<user_id>\d+)', UserBoardSessionViewSet, basename='boardsseesiion')
# router.register(r'user-to-admin(?P<user_id>\d+)', UserToAdminViewSet, basename='user-to-adminas')

# router.register(r'cards', CardViewSet)




urlpatterns = [
    
    path('admin/', admin.site.urls),

    # users
    path('register/',RegisterView.as_view(),name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),

    path('users/', CustomUserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
    path('user-to-s/<int:pk>/', UserToAdminViewSet.as_view({'put': 'user_to_admin'}), name='user_to_admin'),
    path('user-to-admin/<str:username>/', CustomUserDetail.as_view(), name='customuser-detail'),


    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/mark-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),

    # path('comments/create/', CreateCommentView.as_view(), name='create-comment'),

    path('create_board/boards/', AllBardAdminViewSet.as_view({'post': 'create'}), name='create_board'),
    path('update_board/<int:pk>/boards/', AllBardAdminViewSet.as_view({'put': 'update'}), name='update_board'),
    path('invite_user/<int:pk>/boards/', AllBardAdminViewSet.as_view({'post': 'invite_user'}), name='invite_user'),
    path('remove_user/<int:pk>/boards/', AllBardAdminViewSet.as_view({'post': 'remove_user_in_board'}), name='remove_user'),
    path('to/<int:pk>/tugatilmagan/', AllBardAdminViewSet.as_view({'post': 'boar_to_tugatilmagan'}), name='boar_to_tugatilgan'),
    path('to/<int:pk>/bajarilganga/', AllBardAdminViewSet.as_view({'post': 'board_to_bajarilgan'}), name='board_to_bajarilgan'),
    path('to/<int:pk>/bajarilmagan/', AllBardAdminViewSet.as_view({'post': 'board_to_bajarilmagan'}), name='board_to_bajarilmagan'),


    # user

    path('to/<int:pk>/chek/', AllBardUserViewSet.as_view({'post': 'user_to_check_board'}), name='user_to_check_board'),




    path('routers/', include(router.urls)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh')



    # path("api-auth/", include("rest_framework.urls")),
    # path("", include(router.urls))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]


