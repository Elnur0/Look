from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

from .models import Product
from settings.models import Newsletter

emails = Newsletter.objects.all()

@receiver(post_save, sender=Product)
def sendinfo(sender, instance, created, **kwargs):
    if created and emails:
        send_mail(
                "Newsletter",
                f"Hi it is new :) {instance.title}",
                settings.EMAIL_HOST_USER,
                emails,
                fail_silently = False
        )

