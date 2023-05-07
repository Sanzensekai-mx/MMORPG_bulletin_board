from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Reply


@receiver(post_save, sender=Reply)
def notify_post_author_about_reply(sender, **kwargs):
    print(kwargs)
