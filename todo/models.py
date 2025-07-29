from django.db import models
from django.utils.text import slugify
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
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

