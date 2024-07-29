from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, User
from .serializers import TaskSerializer, RegisterSerializer, UserSerializer, UserUpdateSerializer, \
    PasswordChangeSerializer

# Create your views here.
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


class TaskAPIList(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TaskAPICreate(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache_key = f'task_list_{self.request.user.id}'
        cache.delete(cache_key)


class TaskAPIDetail(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache_key = f'task_list_{self.request.user.id}'
        cache.delete(cache_key)

class TaskAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache_key = f'task_list_{self.request.user.id}'
        cache.delete(cache_key)

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache_key = f'user_view_{self.request.user.id}'
        cache.delete(cache_key)


class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            # Удаление кеша пользователя
            cache_key = f'user_view_{user.id}'
            cache.delete(cache_key)
            return Response({'detail': 'Password has been changed.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




