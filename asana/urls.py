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
from trello.views import BoardViewSet, CardViewSet, ListViewSet, ListAllViewSet

from users.views import CustomUserDetailView, CustomUserListCreateView, MarkNotificationAsReadView, NotificationListView, RegisterView, LoginView, LogoutAPIView
from rest_framework.authtoken.views import obtain_auth_token



router = routers.DefaultRouter()
# router.register(r'register', RegistrationAPIView, basename='register')
# router.register(r'login', LoginAPIView, basename='login')
router.register(r'boards', BoardViewSet)
router.register(r'list', ListAllViewSet, basename='list_all_board')
router.register(r'lists/(?P<category_id>\d+)', ListViewSet, basename='texnika')
router.register(r'cards/(?P<category_id>\d+)', CardViewSet, basename='cardd')

# router.register(r'cards', CardViewSet)




urlpatterns = [
    
    path('admin/', admin.site.urls),

    # users
    path('register/',RegisterView.as_view(),name="register"),
    path('login/', obtain_auth_token, name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),

    path('users/', CustomUserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/mark-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),



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


