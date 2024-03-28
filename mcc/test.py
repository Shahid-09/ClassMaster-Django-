from django.db import models

class CourseMaster(models.Model):
    course_name = models.CharField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    isactive = models.BooleanField()

class UserMaster(models.Model):
    # course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True, null=True)
    phone = models.CharField(max_length=13)
    dob = models.DateField()
    city = models.CharField(max_length=150)
    
    SUPERUSER = 'superuser'
    ADMINUSER = 'adminuser'
    STUDENT = 'student'
    CHOICES = [
        (SUPERUSER, 'Superuser'),
        (ADMINUSER, 'Adminuser'),
        (STUDENT, 'Student'),
    ]
    user_type = models.CharField(max_length=20, choices=CHOICES)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    isactive = models.BooleanField()
