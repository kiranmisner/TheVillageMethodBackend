
import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from .managers import CustomUserManager



class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(default ='', max_length=200)
    institution_type = models.CharField(default = '', max_length=30)
    school_id = models.CharField(default='', max_length=6)
    city = models.CharField(default='', max_length=100)
    state = models.CharField(default='', max_length=2)
    website_id = models.IntegerField(default=0)
    def __str__(self):
        return self.name + " (" + str(self.id) + ")"

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default='', max_length=200)

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    is_honors = models.BooleanField(default=False)
    provider = models.CharField(default='', max_length=200, blank=True)
    academic_years = ArrayField(
        base_field=models.CharField(default='', max_length=7),
        default=list,
        blank=True
    )
    grade_levels = ArrayField(
        base_field=models.IntegerField(default=0),
        default=list,
        blank=True
    )
    course_length = models.CharField(default='', max_length=15)
    transcript_abbs = ArrayField(
        base_field=models.CharField(default='', max_length=50),
        default=list,
        blank=True
    )
    subject = models.CharField(default='', max_length=50)
    ag_designation = models.CharField(default='', max_length=1)

    def __str__(self):
        return self.name

class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.00))
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("course", "user")

    def __str__(self):
        return self.value
