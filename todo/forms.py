from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class" : "form-control mr-sm-2",
                "placeholder" : field.label
            })
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if title:
            qs = Task.objects.filter(title__iexact = title)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if not self.instance.pk and qs.exists():
                self.add_error('title', f'{title} is already in use. Please input a new title')
        
        return cleaned_data

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
