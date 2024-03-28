from django.shortcuts import render, redirect
from .forms import LoginForm, AddStudentForm, UpdateStudentForm
from .models import UserMaster, CourseMaster
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return redirect('/login')
            
            return redirect('/dashboard')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
def user_logout(request):
    logout(request)
    return redirect('/login')


def addStudent(request):

    form = ''

    if request.method == 'POST':
        # THE DATA RETURN ENTER BY THE USER IN THE FORM IS STORED HERE
        form = AddStudentForm(request.POST)
        # THIS IS CHECKS IF THE DATA IS VALID OR NOT
        if form.is_valid():
            # THIS IS STORED CLEAN DATA MEANS NEW DATA AND VALID DATA IN THERE RESPECTIVE VARIABLES
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            dob = form.cleaned_data['dob']
            city = form.cleaned_data['city']
            user_type = form.cleaned_data['user_type']
            course = form.cleaned_data['course']

            if course == 'Full Stack':
                course = CourseMaster.objects.get(id=1)

            elif course == 'Front End':
                course = CourseMaster.objects.get(id=2)

            else:
                course = CourseMaster.objects.get(id=3)
            
            # THIS IS INBUILT TABLE(USER) IT IS USE FOR LOGIN OR PASSWORD
            user = User.objects.create_user(username=username, password=password, email=email, is_superuser=False, is_staff=False)

            # THIS IS CREATE OBJECT OF USERMASTER CLASS AND STORE IT IN STUDENT VARIABLE
            student = UserMaster(name=name, email=email, phone=phone, dob=dob, city=city, course=course, created_at=datetime.now(), updated_at=datetime.now(), isactive=True, user_type=user_type)
            # THIS WILL STORED STUDENT OBJECT INTO DATABASE
            student.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            # AFTER INSERTING DATA INTO DATABASE WE WILL RETURN TO DASHBOARD URL
            return redirect('/dashboard')
    else:
        # its the store the blank form in the form variable
        form = AddStudentForm()
        # THIS IS RETURN WITH BLANK FORM, WHEN WE MAKE GET REQUEST SAME AS BELOW COMMENT
    return render(request, 'add.html', {'form': form})

@login_required(login_url='/login')

def dashboard(request):
    user = request.user
    if user.groups.filter(name='student').exists():
        std_email = user.email
        std_details = UserMaster.objects.filter(email=std_email).values()
        course = ''
        for i in std_details:
            if i['course_id'] == 1:
                course = 'Full Stack'

            elif i['course_id'] == 2:
                course = 'Front End'

            else:
                course = 'Back End'

        dict = {
            'is_student': True,
            'details': std_details,
            'course': course
        }

        return render(request, 'dashboard.html', dict)
    
    if request.method == 'POST':
        # It give me the value of the button which is click 
        value = request.POST.get('btn')
        
        if value == 'Edit Student':
            return redirect('/editstudent')

        if value == 'Add Student':
             return redirect('/addstudent')

    # IF THE BUTTON IS CLICKED BY THE USER TO SEARCH STUDENT THEN 
        if value == 'Search Student':
            # FIRST WE WILL CHECK WHICH COURSE USER HAS SELECTED 
            course = request.POST.get('course')
            id = 0
            if course == 'Full Stack':
                id = 1
            elif course == 'Front End':
                id = 2
            else:
                id = 3

            # WE WILL MAKE A LIST OF ALL THE STUDENT DICTIONARY THAT HAVE THE SELECTED COURSE 
            stds = UserMaster.objects.filter(course_id=id).values()
            return render(request, 'dashboard.html', {'stds': stds})
            
   # when we enter url in the browser we make a get request which is handle by this return function
    return render(request, 'dashboard.html', {})

# This is for edit Student

@login_required(login_url='/login')

def editStudent(request, id=0):
    if id != 0:
        if request.method == 'POST':
            form = UpdateStudentForm(request.POST)
        # THIS IS CHECKS IF THE DATA IS VALID OR NOT
            if form.is_valid():
                # THIS IS STORED CLEAN DATA MEANS NEW DATA AND VALID DATA IN THERE RESPECTIVE VARIABLES
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                dob = form.cleaned_data['dob']
                city = form.cleaned_data['city']
                user_type = form.cleaned_data['user_type']
                course = form.cleaned_data['course']

                if course == 'Full Stack':
                    course = CourseMaster.objects.get(id=1)

                elif course == 'Front End':
                    course = CourseMaster.objects.get(id=2)

                else:
                    course = CourseMaster.objects.get(id=3)

                UserMaster.objects.filter(id=id).update(name=name, email=email, phone=phone, dob=dob, city=city, course=course, user_type=user_type)
        
            
        else:
            std = UserMaster.objects.get(id=id)
            details = {
                'name': std.name,
                'city': std.city,
                'phone': std.phone,
                'email': std.email,
                'dob': std.dob,
            }

            form = UpdateStudentForm(initial=details)
            print(form)
            return render(request, 'update.html', {'form': form})
    
    allStudents = UserMaster.objects.all().values()
    return render(request, 'edit.html', {'all': allStudents})




