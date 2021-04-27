from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default='users/default.jpg', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.first_name)


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = urlsafe_base64_encode(force_bytes(User.objects.count() + 1))
        instance.is_active = False


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


