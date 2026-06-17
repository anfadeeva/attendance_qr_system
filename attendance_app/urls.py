from django.urls import path
from . import views

app_name = 'attendance_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_session, name='create_session'),
    path('qr/<uuid:session_id>/', views.session_qr, name='show_qr'),
    path('report/', views.attendance_report, name='report'),

    path('mark/', views.mark_attendance, name='manual_mark'),
    path('mark/<uuid:session_id>/', views.mark_attendance, name='mark_attendance'),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', views.password_change, name='password_change'),
    path('my_report/', views.student_report, name='student_report'),
]
