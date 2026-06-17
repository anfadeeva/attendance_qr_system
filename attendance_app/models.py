# attendance_app/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User

# Роли пользователей
ROLE_CHOICES = [
    ('student', 'Студент'),
    ('teacher', 'Преподаватель'),
    ('admin', 'Администратор'),
]

class Group(models.Model):
    """Учебная группа (например, ИС-31)."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    """
    Расширение стандартной модели User.
    Хранит роль и дополнительные данные.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=64, blank=True, null=True)  # номер зачётки
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return f"{self.user.username} ({self.role})"



class Subject(models.Model):
    """Дисциплина, привязанная к группе."""
    title = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.title} - {self.group.name}"


class Session(models.Model):
    """
    Учебное занятие (сессия для отметки посещаемости).
    UUID используется как первичный ключ для безопасности.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sessions')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'teacher'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.title} ({self.start_time.strftime('%d.%m.%Y %H:%M')})"


class Attendance(models.Model):
    """Факт присутствия студента на занятии."""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'student'})
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'student')  # Запрет повторной отметки

    def __str__(self):
        return f"{self.student.username} - {self.session}"