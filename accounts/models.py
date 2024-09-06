from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, role, phone_no, password=None, password2=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
            phone_no=phone_no
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,  password=None):
        user = self.create_user(
            email,
            name=name,
            role=0,
            phone_no='1234567890',
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=30)
    ROLE_CHOICES = (
        (1, 'Farmer'),
        (2, 'Buyer'),
    )

    role = models.IntegerField(choices=ROLE_CHOICES)
    phone_no = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
