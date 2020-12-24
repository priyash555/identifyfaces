from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.

class TestImages(models.Model):
    GroupImage = models.ImageField(upload_to='train', height_field=None, width_field=None, max_length=None)
    PersonImage = models.ImageField(upload_to='test', height_field=None, width_field=None, max_length=None)
    ResultImage = models.ImageField(upload_to='test', height_field=None, width_field=None, max_length=None, blank=True)

@receiver(post_delete, sender=TestImages)
def submission_delete(sender, instance, **kwargs):
    instance.GroupImage.delete(False) 
    instance.PersonImage.delete(False) 
