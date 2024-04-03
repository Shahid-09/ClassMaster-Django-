from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('dashboard/', views.dashboard),
    path('addstudent/', views.addStudent),
    path('editstudent/', views.editStudent),
    path('mycourse/', views.myCourse),
    path('editstudent/<int:id>/', views.editStudent),
    path('delstudent/<int:id>/', views.delStudent),
    path('', views.homePage),

]