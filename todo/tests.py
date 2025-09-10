from django.test import TestCase
from .models import Task
from django.utils.text import slugify

# Create your tests here.

class TodoTestCase(TestCase):
    def setUp(self):
        self.number_of_tasks = 7
        for i in range(0, self.number_of_tasks):
            Task.objects.create(title="Go to bed")
    
    def test_task_exists(self):
        qs = Task.objects.all()
        self.assertTrue(qs.exists())

    def test_task_count(self):
        qs = Task.objects.all()
        self.assertEqual(qs.count(), 7)    
    
    def test_go_to_bed(self):
        task = Task.objects.all().order_by('id').first()
        title = task.title
        slug = task.slug
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title)
    
    def test_unique_go_to_bed(self):
        qs = Task.objects.exclude(slug__iexact='go-to-bed')

        for task in qs:
            title = task.title
            slug = task.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)
