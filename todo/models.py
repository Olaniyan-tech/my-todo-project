from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import slugify_instance_title
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

#signals    
def todo_pre_save(sender, instance, *args, **kwargs):
    print('Pre_save...')
    if not instance.slug:
        slugify_instance_title(instance, save=False)

pre_save.connect(todo_pre_save, sender=Task)


def todo_post_save(sender, instance, created, *args, **kwargs):
    print('Post_save...')
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(todo_post_save, sender=Task)




