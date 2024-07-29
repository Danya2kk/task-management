"""
URL configuration for task_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .yasg import urlpatterns as doc_urls
from tasks.views import *
from debug_toolbar.toolbar import debug_toolbar_urls

'''
Реализуйте следующие API endpoints:

Регистрация нового пользователя (/api/register/)
Логин пользователя с выдачей JWT токена (/api/login/)
Получение информации о текущем пользователе с использованием JWT токена (/api/user/)
Создание новой задачи (/api/tasks/create/)
Получение списка задач текущего пользователя (/api/tasks/)
Обновление задачи (/api/tasks/<id>/update/)
Удаление задачи (/api/tasks/<id>/delete/)
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/drf-auth/', include('rest_framework.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', RegisterAPIView.as_view()),
    path('api/user/update/', UserAPIUpdate.as_view()),
    path('api/user/password/', PasswordChangeView.as_view()),
    path('api/user/', UserAPIView.as_view()),
    path('api/tasks/', TaskAPIList.as_view()),
    path('api/tasks/<int:pk>/', TaskAPIDetail.as_view()),
    path('api/tasks/create/', TaskAPICreate.as_view()),
    path('api/tasks/<int:pk>/update/', TaskAPIUpdate.as_view()),
    path('api/tasks/<int:pk>/delete/', TaskAPIDestroy.as_view())
] + doc_urls + debug_toolbar_urls()



