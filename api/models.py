"""
Summary:
    Represents the necessary model classes for this backend framework. These classes are the bridge between the Django
    REST framework and both the Postgresql/Salesforce databases, as they specify the format of each table on these
    databases.
"""
import uuid
import salesforce
# TODO: Add the below dependency when ready to create the Grade model
# from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from .managers import CustomUserManager

class School(salesforce.models.SalesforceModel):
    """
    Summary:
        Model that represents a School from the A-G School List on the Salesforce system.

    TODO: Modify ID representation to allow for POST requests through the REST API
    """
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

class CustomUser(AbstractUser):
    """ 
    Summary: 
        Model that represents a custom User for our system. This extends the AbstractUser class from
        django.contrib.auth.models.

    TODO: Link users to their statistics (GPA, Course completion stats, etc)
    """
    # Utilizes a random UUID through the UUIDField from django.db.models
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Since we will be using emails for usernames, the username field is set to None
    username = None
    email = models.EmailField('email address', unique=True)
    name = models.CharField(default="", max_length=200)
    # Represents unique ID for a school (found in Salesforce) as a CharField
    school = models.CharField(default="", max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email + ", is_superuser: " + str(self.is_superuser)

class UserAccount(salesforce.models.SalesforceModel):
    """ 
    Summary:
        Model that represents a custom User on the Salesforce system.

    TODO: This model should be linked directly to the CustomUser representation by an external ID
    TODO: This model should be updated every time a CustomUser is modified (override serializer methods in the 
            CustomUserSerializer class)
    TODO: Modify ID representation to allow for POST requests through the REST API
    """
    name = salesforce.models.CharField(max_length=200, default="", db_column="Name")
    email = salesforce.models.EmailField('email address', default="", db_column="Email__c", unique=True)
    school = salesforce.models.ForeignKey(School, db_column="High_School__c", on_delete=models.PROTECT)

    def __str__(self):
        return self.name + " (" + str(self.id) + ")"

    class Meta:
        # The corresponding name for the database table in Salesforce
        db_table = "User_Account__c"

class Course(salesforce.models.SalesforceModel):
    """ 
    Summary:
        Model that represents a Course from any of the A-G schools on the Salesforce system.

    TODO: Modify ID representation to allow for POST requests through the REST API
    """
    id = salesforce.models.CharField(max_length=18, primary_key=True, db_column="Id", editable=False, serialize=False,
                                     auto_created=True)
    name = salesforce.models.CharField(default='', db_column='Name', max_length=200)
    school = salesforce.models.ForeignKey(School, db_column='High_School__c', on_delete=models.PROTECT)
    is_honors = salesforce.models.BooleanField(default=False, db_column='Is_Honors__c', blank=True)
    provider = salesforce.models.CharField(default='', db_column='Provider__c', max_length=200, blank=True)
    academic_years = salesforce.models.CharField(default='', db_column='Academic_Years__c', max_length=200, blank=True)
    grade_levels = salesforce.models.CharField(default='', db_column='Grade_Levels__c', max_length=200, blank=True)
    course_length = salesforce.models.CharField(default='', db_column='Course_Length__c', max_length=15, blank=True)
    transcript_abbs = salesforce.models.CharField(default='', db_column='Transcript_Abbs__c', max_length=200,
                                                  blank=True)
    subject = salesforce.models.CharField(default='', db_column='Subject__c', max_length=50, blank=True)
    ag_designation = models.CharField(default='', db_column='AG_Designation__c', max_length=1, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Course__c"
        
"""
TODO: Implement a Grade model, similar to this format, on Salesforce and link on Django through 
      salesforce.models.SalesforceModel

class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.00))
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("course", "user")

    def __str__(self):
        return self.value
"""
