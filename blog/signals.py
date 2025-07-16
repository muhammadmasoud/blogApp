from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
