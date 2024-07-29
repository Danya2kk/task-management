from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import User, Task

@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def clear_task_cache(sender, instance, **kwargs):
    cache_key = f'task_list_{instance.user.id}'
    cache.delete(cache_key)

@receiver(post_save, sender=User)
def clear_user_cache(sender, instance, **kwargs):
    cache_key = f'user_view_{instance.id}'
    cache.delete(cache_key)
