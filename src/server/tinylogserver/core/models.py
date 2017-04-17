from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone


class TinyLogUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create(self, username, password, **extra_fields):
        return self.create_user(username, password, **extra_fields)

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class TinyLogUser(AbstractBaseUser, PermissionsMixin):
    """Tiny Log User Model"""
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=30,
        unique=True,
        help_text='Required. <30 chars. Alphanumeric and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    display_name = models.CharField(
        'display_name',
        max_length=30,
        null=True,
        help_text='Optional. <30 chars. Alphanumeric and @/./+/-/_ only.',
        validators=[username_validator],
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
            'Designates whether this user should be treated as active. ' \
            'Unselect this instead of deleting accounts.'
        ,
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = TinyLogUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.display_name or self.username

    def get_short_name(self):
        return self.display_name or self.username

    def email_user(self, *args, **kwargs):
        pass


class TinyLog(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(TinyLogUser)

    def __str__(self):
        return 'TinyLog(id={}, name={})'.format(self.id, self.name)

    @property
    def log_entries(self):
        return [entry
            for entry in TinyLogEntry.objects.filter(tiny_log=self).\
                order_by('-date_logged')]


class TinyLogEntry(models.Model):
    tiny_log = models.ForeignKey(TinyLog, on_delete=models.CASCADE)
    created_by = models.ForeignKey(TinyLogUser)
    text_content = models.CharField(max_length=500)
    date_logged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'TinyLogEntry(parent_id={}, text_content={})'.format(
            self.tiny_log.id, self.text_content)
