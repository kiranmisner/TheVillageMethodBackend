"""
Summary:
    Represents the necessary serializer classes for this backend framework. These classes handle the necessary
    operations for creating and updating model instances on both Postgresql and Salesforce databases.
"""
import copy

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import School, Course, UserAccount

# Get the appropriate custom user model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """ 
    Summary:
        Represents a serializer class for the CustomUser model. This class is responsible for serializing data from the
        REST API through the corresponding CRUD operations.
    """
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def format_validated_data_for_sf(self, validated_data):
        """
        Summary:
            Helper method to formate the validated_data dictionary captured by the create and update methods properly
            before serializing into the Salesforce database.

        Args:
            validated_data (dict): The named keyword arguments that make up a CustomUser instance, captured into a 
                                   dictionary.
        
        Returns:
            dict: The updated version of validated_data, formatted for serialization in Salesforce.

        TODO: Thoroughly test this method to ensure it works properly.
        """
        new_validated_data = copy.deepcopy(validated_data)
        if 'school' in new_validated_data.keys():
            school_id = new_validated_data['school']
            del new_validated_data['school']
            new_validated_data['school'] = School.objects.get(pk=school_id)
        if 'password' in new_validated_data.keys():
            del new_validated_data['password']
        return new_validated_data

    def create(self, validated_data):
        """ 
        Summary:
            Overridden create method from serializers.ModelSerializer that follows the expected creation behavior, but
            also creates a UserAccount object on the Salesforce database.
            The REST framework will automatically call this method when serializing a CustomUser instance.

        Args:
            validated_data (dict): The named keyword arguments that make up a CustomUser instance, captured into a 
                                   dictionary.

        Returns:
            CustomUser: The new CustomUser instance that was created (on Postgresql).

        TODO: Thoroughly test this method to ensure it works properly.
        """
        # user = User.objects.create(**validated_data)
        user = super().create(validated_data)
        # Save into Salesforce database
        print(validated_data)
        UserAccount.objects.create(**self.format_validated_data_for_sf(validated_data))
        return user

    def update(self, instance, validated_data):
        """ 
        Summary:
            Overridden update method from serializers.ModelSerializer that follows the expected update behavior, but
            also updates the given UserAccount object on the Salesforce database using the email as an external ID.
            The REST framework will automatically call this method when updating a serialized CustomUser instance.

        Args:
            validated_data (dict): The named keyword arguments that make up a CustomUser instance, captured into a 
                                   dictionary.

        Returns:
            CustomUser: The CustomUser instance that was updated (on Postgresql).

        TODO: Thoroughly test this method to ensure it works properly.
        """
        serializers.ModelSerializer.update
        super().update(instance, validated_data)
        # Update in Salesforce database
        UserAccount.objects.get(email=instance.email).update(**self.format_validated_data_for_sf(validated_data))
        return instance

    class Meta:
        """
        Summary: 
            Meta subclass that specifies relevant fields to serialize from the appropriate model.
        """
        model = User
        fields = ['id', 'email', 'password', 'token', 'name', 'school']

class UserAccountSerializer(serializers.ModelSerializer):
    """
    Summary:
        Represents a serializer class for the UserAccount model. Extends serializers.ModelSerializer from the Django
        REST framework.
    """

    class Meta:
        """
        Summary: 
            Meta subclass that specifies relevant fields to serialize from the appropriate model.
        """
        model = UserAccount
        fields = ['id', 'name', 'school']

class SchoolSerializer(serializers.ModelSerializer):
    """
    Summary:
        Represents a serializer class for the School model. Extends serializers.ModelSerializer from the Django REST
        framework.
    """
    class Meta:
        """
        Summary: 
            Meta subclass that specifies relevant fields to serialize from the appropriate model.
        """
        model = School
        fields = ['id', 'name', 'institution_type', 'school_id', 'city', 'state', 'website_id']

class CourseSerializer(serializers.ModelSerializer):
    """
    Summary:
        Represents a serializer class for the Course model. Extends serializers.ModelSerializer from the Django REST
        framework.
    """
    class Meta:
        """
        Summary: 
            Meta subclass that specifies relevant fields to serialize from the appropriate model.
        """
        model = Course
        fields = ['id', 'name', 'school', 'is_honors', 'provider', 'academic_years', 'grade_levels', 'course_length',
            'transcript_abbs', 'subject', 'ag_designation']

class SchoolCoursesSerializer(serializers.ModelSerializer):
    """
    Summary:
        Represents a serializer class for the School model, where the only listed field is the corresponding set of
        related Course instances.
    """
    course_set = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        """
        Summary: 
            Meta subclass that specifies relevant fields to serialize from the appropriate model.
        """
        model = School
        fields = ['course_set']

"""
TODO: Write a serializer class for the Grade model, such that each Grade is serialized and linked properly to a Course
      and a CustomUser instance, similar to the example shown below.

class GradeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Grade
        fields = ['id', 'value', 'course', 'user']

    def get_user(self, obj):
        return obj.user.id
"""
