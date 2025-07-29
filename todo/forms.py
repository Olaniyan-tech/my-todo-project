from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
    
    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        qs = Task.objects.filter(title__icontains = title)
        if qs.exists():
            self.add_error('title', f'{title} is already in use. Please input a new title')

class TaskFormold(forms.Form):
    title = forms.CharField()
    #completed = forms.BooleanField()
    #date_created = forms.DateTimeField()

    """
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and title.lower().strip() == "go to bed":
           raise forms.ValidationError ('The title is taken')
        print("Title: ", title)
        return title
    """
