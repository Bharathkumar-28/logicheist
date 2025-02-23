# adminpanel/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from adminpanel.models import UserActivity

@receiver(post_save, sender=User)
def create_user_activity(sender, instance, created, **kwargs):
    if created:
        # Create a new UserActivity record for the newly created user
        UserActivity.objects.create(
            user=instance,
            last_active=timezone.now()  # You can set last_active to the current time
        )
        print(f"Created UserActivity for {instance.username}")
