from django.db import models
from django.contrib.auth.models import AbstractUser

'''
Модель пользователя должна содержать стандартные поля для регистрации и аутентификации.

Модель задачи должна содержать поля: название задачи, описание, дата создания, дата завершения,
 статус (новая, в процессе, завершена) и ссылка на пользователя, которому она принадлежит.
'''
# Create your models here.


class User(AbstractUser):
    pass


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
