from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import School, Course

User = get_user_model()

class SchoolSerializer(serializers.ModelSerializer):
    # courses = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())

    class Meta:
        model = School
        fields = ['id', 'name', 'institution_type', 'school_id', 'city', 'state', 'website_id']

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'school', 'is_honors', 'provider', 'academic_years', 'grade_levels', 'course_length',
            'transcript_abbs', 'subject', 'ag_designation']