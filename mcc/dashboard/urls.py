from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard),
    path('addstudent/', views.addStudent),
    path('editstudent/', views.editStudent),
    path('editstudent/<int:id>/', views.editStudent),

]