from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from .managers import CustomUserManager
from .models import School, Course, Grade

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'token']

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'name', 'institution_type', 'school_id', 'city', 'state', 'website_id']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'school', 'is_honors', 'provider', 'academic_years', 'grade_levels', 'course_length',
            'transcript_abbs', 'subject', 'ag_designation']

class SchoolCoursesSerializer(serializers.ModelSerializer):
    course_set = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = School
        fields = ['course_set']

class GradeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Grade
        fields = ['id', 'value', 'course', 'user']

    def get_user(self, obj):
        return obj.user.id