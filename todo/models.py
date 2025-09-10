from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from .utils import slugify_instance_title

# Create your models here.

User = settings.AUTH_USER_MODEL

class TaskQueryset(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains = query)
        return self.filter(lookups)

class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQueryset(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query=query)
        
class Task(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
    
    objects = TaskManager() 

    def get_absolute_url(self):
        return reverse('todo:details', kwargs={'slug' : self.slug})
    
    def get_edit_url(self):
        return reverse('todo:update', kwargs={'id' : self.id})
    
    def get_delete_url(self):
        return reverse('todo:delete', kwargs={'id' : self.id})
    
    def all_task_url(self):
        return reverse('todo:all-tasks')
    
    # def save(self, *args, **kwargs):
    #     slugify_instance_title(self, save=False)
    #     super().save(*args, **kwargs)

#signals    
def todo_pre_save(sender, instance, *args, **kwargs):
    if instance.title:
        slugify_instance_title(instance, save=False)

pre_save.connect(todo_pre_save, sender=Task)


# def todo_post_save(sender, instance, created, *args, **kwargs):
#     if created and not instance.slug:
#         slugify_instance_title(instance, save=True)

# post_save.connect(todo_post_save, sender=Task)




