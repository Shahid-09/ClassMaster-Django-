from django.db import models

class CourseMaster(models.Model):
    course_name = models.CharField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    isactive = models.BooleanField()

    def __str__(self):
        return self.course_name

class UserMaster(models.Model):
    course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE, default='', null=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True, null=True)
    phone = models.CharField(max_length=13)
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=150)
    
    SUPERUSER = 'superuser'
    ADMINUSER = 'adminuser'
    STUDENT = 'student'
    CHOICES = [
        (SUPERUSER, 'Superuser'),
        (ADMINUSER, 'Adminuser'),
        (STUDENT, 'Student'),
    ]
    user_type = models.CharField(max_length=20, choices=CHOICES, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    isactive = models.BooleanField(null=True)

    def __str__(self):
            return self.name
