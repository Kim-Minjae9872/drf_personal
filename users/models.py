from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, email, fullname, nickname, password=None):
        if not email or not password or not username:
            raise ValueError(
                "Users must have an email address and password and username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            fullname=fullname,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, fullname, nickname, password=None):
        user = self.create_user(
            email=email,
            username=username,
            fullname=fullname,
            nickname=nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(
        verbose_name="email_address",
        max_length=255,
    )
    fullname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True)
    birthday = models.DateField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "fullname", "nickname"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
