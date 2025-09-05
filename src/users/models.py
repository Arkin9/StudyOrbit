from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email = email,
            username = username,
            password = password,
        )
        user.role = User.ADMIN
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    ADMIN = 'Admin'
    HOD = 'HOD'
    TEACHER = 'Teacher'
    STUDENT = 'Student'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (HOD, 'Head of Department'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]


    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Ensure this is defined
    is_superuser = models.BooleanField(default=False)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]


    def __str__(self):
        return self.first_name

    def is_admin(self):
        return self.role == self.ADMIN

    def is_hod(self):
        return self.role == self.HOD

    def is_teacher(self):
        return self.role == self.TEACHER

    def is_student(self):
        return self.role == self.STUDENT
