import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

DEFAULT_PROFILE_PICTURE = '/profile_picture/default.jpg'

# Create your models here.


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_picture', default=DEFAULT_PROFILE_PICTURE)
    
    def __str__(self):
        return self.username


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.profile_picture and instance.profile_picture.name != DEFAULT_PROFILE_PICTURE:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)
    # if instance.file:
    #     if os.path.isfile(instance.file.path):
    #         os.remove(instance.file.path)

class Post(models.Model):
    caption = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="post/")
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
