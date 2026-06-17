from django.db import models
from django.contrib.auth.models import User
import uuid

ROLE_CHOICES = [
    ('student', 'Студент'),
    ('teacher', 'Преподаватель'),
    ('admin', 'Администратор'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} — {self.group}"

# Модель Session (занятие)
class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Уникальный ID для сессии
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Связь с предметом
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'teacher'})  # Только для учителей
    start_time = models.DateTimeField()  # Время начала
    end_time = models.DateTimeField(blank=True, null=True)  # Время окончания 
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания сессии

    # Явно указываем приложение, к которому относится модель
    class Meta:
        app_label = 'attendance_app'

    def __str__(self):
        return f"Session {self.id} — {self.subject.title} ({self.start_time})"

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'student'})
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.username} at {self.session.id}"
