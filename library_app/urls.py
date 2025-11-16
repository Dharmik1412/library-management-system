from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    path('add_book/', views.add_book, name='add_book'),
    path('add_student/', views.add_student, name='add_student'),
    path('issue_book/', views.issue_book, name='issue_book'),
]
