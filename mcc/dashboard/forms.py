from django import forms
from django.contrib.auth.forms import UserCreationForm

# WHEN WE WANT GET DATA FROM USER WE USE DJANGO INBUILT FORM TO MAKE DATA VALIDATION AND OHTER THING IS HERE

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput())

class AddStudentForm(UserCreationForm):
    name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=200)
    phone = forms.CharField(max_length=13)
    dob = forms.DateField()
    city = forms.CharField(max_length=150)
    CHOICES = (('Front End', 'Front End'),
                ('Back End', 'Back End'), 
                ('Full Stack', 'Full Stack'))
    course = forms.ChoiceField(choices=CHOICES)
    user_types = (('superuser', 'superuser'), ('adminuser', 'adminuser'), ('student', 'student'))
    user_type = forms.ChoiceField(choices=user_types)

class UpdateStudentForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=200)
    phone = forms.CharField(max_length=13)
    dob = forms.DateField()
    city = forms.CharField(max_length=150)
    CHOICES = (('Front End', 'Front End'),
                ('Back End', 'Back End'), 
                ('Full Stack', 'Full Stack'))
    course = forms.ChoiceField(choices=CHOICES)
    user_types = (('superuser', 'superuser'), ('adminuser', 'adminuser'), ('student', 'student'))
    user_type = forms.ChoiceField(choices=user_types)
    