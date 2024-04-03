from django.shortcuts import render, redirect
from .forms import LoginForm, AddStudentForm, UpdateStudentForm, SignUpForm
from .models import UserMaster, CourseMaster
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

# THIS IS MY LOGIN FUNCTION
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return redirect("/login")

            return redirect("/dashboard")
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})

# THIS IS MY SIGNUP FUNCTION
def user_signup(request):

    form = ""

    if request.method == "POST":
        # THE DATA RETURN ENTER BY THE USER IN THE FORM IS STORED HERE
        form = SignUpForm(request.POST)
        # THIS IS CHECKS IF THE DATA IS VALID OR NOT
        if form.is_valid():
            # THIS IS STORED CLEAN DATA MEANS NEW DATA AND VALID DATA IN THERE RESPECTIVE VARIABLES
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_superuser=False,
                is_staff=False,
            )
            group = Group.objects.get(name="student")
            user.groups.add(group)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return redirect("/login")

            return redirect("/dashboard")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


# THIS IS MY LOGOUT FUNCTION
def user_logout(request):
    logout(request)
    return redirect("/")

# THIS IS MY ADD STUDENT FUNCTION
@login_required(login_url="/login")
def addStudent(request):

    form = ""

    if request.method == "POST":
        # THE DATA RETURN ENTER BY THE USER IN THE FORM IS STORED HERE
        form = AddStudentForm(request.POST)
        # THIS IS CHECKS IF THE DATA IS VALID OR NOT
        if form.is_valid():
            # THIS IS STORED CLEAN DATA MEANS NEW DATA AND VALID DATA IN THERE RESPECTIVE VARIABLES
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            dob = form.cleaned_data["dob"]
            city = form.cleaned_data["city"]
            user_type = form.cleaned_data["user_type"]
            course = form.cleaned_data["course"]

            if course == "Full Stack":
                course = CourseMaster.objects.get(id=1)

            elif course == "Front End":
                course = CourseMaster.objects.get(id=2)

            else:
                course = CourseMaster.objects.get(id=3)

            # THIS IS CREATE OBJECT OF USERMASTER CLASS AND STORE IT IN STUDENT VARIABLE
            student = UserMaster(
                name=name,
                email=email,
                phone=phone,
                dob=dob,
                city=city,
                course=course,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                isactive=True,
                user_type=user_type,
            )
            # THIS WILL STORED STUDENT OBJECT INTO DATABASE
            student.save()

            # AFTER INSERTING DATA INTO DATABASE WE WILL RETURN TO DASHBOARD URL
            return redirect("/dashboard")
    else:
        # IT IS STORE THE BLANK FORM IN THE FORM VARIABLE 
        form = AddStudentForm()
        # THIS IS RETURN WITH BLANK FORM, WHEN WE MAKE GET REQUEST SAME AS BELOW COMMENT
    return render(request, "add.html", {"form": form})

# THIS IS MY COURSE AND DETAILS OF STUDENT FUNCTION
@login_required(login_url="/login")
def myCourse(request):
    user = request.user
    if user.groups.filter(name="student").exists():
        std_email = user.email
        std_details = UserMaster.objects.filter(email=std_email).values()
        course = ""
        for i in std_details:
            if i["course_id"] == 1:
                course = "Full Stack"

            elif i["course_id"] == 2:
                course = "Front End"

            else:
                course = "Back End"

        dict = {"is_student": True, "details": std_details, "course": course}

        return render(request, "mycourse.html", dict)

# THIS IS MY DASHBOARD FUNCTION
@login_required(login_url="/login")
def dashboard(request):
    user = request.user
    if user.groups.filter(name="student").exists():
        if request.method == "POST":
            return redirect("/mycourse")
        return render(request, "dashboard.html", {"is_student": True})

    if request.method == "POST":
        # IT GIVE ME THE VALUE OF THE BUTTON WHICH IS CLICK 
        value = request.POST.get("btn")

        if value == "Edit Student":
            return redirect("/editstudent")

        if value == "Add Student":
            return redirect("/addstudent")

        # IF THE BUTTON IS CLICKED BY THE USER TO SEARCH STUDENT THEN
        if value == "Search Student":
            # FIRST WE WILL CHECK WHICH COURSE USER HAS SELECTED
            course = request.POST.get("course")
            id = 0
            if course == "Full Stack":
                id = 1
            elif course == "Front End":
                id = 2
            else:
                id = 3
            print(id)

            # WE WILL MAKE A LIST OF ALL THE STUDENT DICTIONARY THAT HAVE THE SELECTED COURSE
            stds = UserMaster.objects.filter(course_id=id).values()
            return render(request, "dashboard.html", {"stds": stds})

    # WHEN WE ENTER URL IN THE BROWSER WE MAKE A GET REQUEST WHICH IS HANDLE BY THE RETURN FUNCTION 
    return render(request, "dashboard.html", {})

# THIS IS MY EDIT STUDENT FUNCTION
@login_required(login_url="/login")
def editStudent(request, id=0):
    if id != 0:
        if request.method == "POST":
            form = UpdateStudentForm(request.POST)
            # THIS IS CHECKS IF THE DATA IS VALID OR NOT
            if form.is_valid():
                # THIS IS STORED CLEAN DATA MEANS NEW DATA AND VALID DATA IN THERE RESPECTIVE VARIABLES
                name = form.cleaned_data["name"]
                email = form.cleaned_data["email"]
                phone = form.cleaned_data["phone"]
                dob = form.cleaned_data["dob"]
                city = form.cleaned_data["city"]
                user_type = form.cleaned_data["user_type"]
                course = form.cleaned_data["course"]

                if course == "Full Stack":
                    course = CourseMaster.objects.get(id=1)

                elif course == "Front End":
                    course = CourseMaster.objects.get(id=2)

                else:
                    course = CourseMaster.objects.get(id=3)

                UserMaster.objects.filter(id=id).update(
                    name=name,
                    email=email,
                    phone=phone,
                    dob=dob,
                    city=city,
                    course=course,
                    user_type=user_type,
                )

        else:
            std = UserMaster.objects.get(id=id)
            details = {
                "name": std.name,
                "city": std.city,
                "phone": std.phone,
                "email": std.email,
                "dob": std.dob,
            }

            form = UpdateStudentForm(initial=details)
            print(form)
            return render(request, "update.html", {"form": form})

    allStudents = UserMaster.objects.all().values()
    return render(request, "edit.html", {"all": allStudents})

# THIS IS MY DELETE STUDENT FUNCTION
@login_required(login_url="/login")
def delStudent(request, id=0):
    if id != 0:
        std = UserMaster.objects.get(id=id)
        email = std.email
        user = User.objects.get(email=email)
        std.delete()
        user.delete()

    return redirect("/editstudent")

# THIS IS MY HOME PAGE FUNCTION
def homePage(request):
    return render(request, "home.html", {})
