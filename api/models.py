
import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
import salesforce

from .managers import CustomUserManager

class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None
    email = models.EmailField('email address', unique=True)
    # school = models.ForeignKey(School, on_delete=models.CASCADE)
    # Need to add user stats (GPA, Course completion stats)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class School(salesforce.models.SalesforceModel):
    id = salesforce.models.CharField(max_length=18, primary_key=True, db_column="Id", editable=False, serialize=False, auto_created=True)
    name = salesforce.models.CharField(default="", db_column="Name", max_length=200)
    institution_type = salesforce.models.CharField(default="", db_column="Institution_Type__c", max_length=30)
    school_id = salesforce.models.CharField(default="", unique=True, db_column='School_ID__c', max_length=6)
    city = salesforce.models.CharField(default="", db_column='City__c', max_length=100)
    state = salesforce.models.CharField(default="", db_column='State__c', max_length=2)
    website_id = salesforce.models.IntegerField(default=0, unique=True, db_column='Website_ID__c')

    def __str__(self):
        return self.name + " (" + str(self.id) + ")"
    
    class Meta:
        db_table = "HighSchool__c"

class Course(salesforce.models.SalesforceModel):
    id = salesforce.models.CharField(max_length=18, primary_key=True, db_column="Id", editable=False, serialize=False, auto_created=True)
    name = salesforce.models.CharField(default='', db_column='Name', max_length=200)
    school = salesforce.models.ForeignKey(School, db_column='High_School__c', on_delete=models.PROTECT)
    is_honors = salesforce.models.BooleanField(default=False, db_column='Is_Honors__c', blank=True)
    provider = salesforce.models.CharField(default='', db_column='Provider__c', max_length=200, blank=True)
    academic_years = salesforce.models.CharField(default='', db_column='Academic_Years__c', max_length=200, blank=True)
    grade_levels = salesforce.models.CharField(default='', db_column='Grade_Levels__c', max_length=200, blank=True)
    course_length = salesforce.models.CharField(default='', db_column='Course_Length__c', max_length=15, blank=True)
    transcript_abbs = salesforce.models.CharField(default='', db_column='Transcript_Abbs__c', max_length=200, blank=True)
    subject = salesforce.models.CharField(default='', db_column='Subject__c', max_length=50, blank=True)
    ag_designation = models.CharField(default='', db_column='AG_Designation__c', max_length=1, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Course__c"

class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.00))
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("course", "user")

    def __str__(self):
        return self.value
