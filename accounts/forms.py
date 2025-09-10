from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    error_messages = {"password_mismatch" : "Password doesn't match. Try again"}

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
        
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")

    #     if password1 and password2 and password1 != password2:
    #         self.add_error("password2", "Password doesn't match. Try again")
        
    #     return cleaned_data
        

    