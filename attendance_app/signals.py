# attendance_app/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Создаёт профиль при создании пользователя, если его ещё нет.
    Обновляет профиль при изменении пользователя.
    """
    if created:
        # get_or_create гарантирует, что дубликат не возникнет
        Profile.objects.get_or_create(user=instance)
    else:
        # Если профиль уже есть, сохраняем его (на случай изменений)
        if hasattr(instance, 'profile'):
            instance.profile.save()