"""
Summary:
    Represents the necessary viewset classes for this backend framework. These classes represent the available
    endpoints for interacting with the backend.
"""
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny # TODO: Add IsAdminUser when ready to create the GradeView class
# TODO: Add the below dependencies when ready to create the GradeView class
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListCreateAPIView, CreateAPIView

from .models import School, Course
from .serializers import SchoolSerializer, CourseSerializer, SchoolCoursesSerializer, UserSerializer

# class CreateUserViewSet(viewsets.ModelViewSet):
class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Summary:
        Represents a Model viewset for the CustomUser model. Provides a create operation for user accounts.
    """
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class SchoolCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Summary:
        Represents a Model viewset for the School model (course list only). Provides read-only operations for school
        course lists.
    """
    queryset = School.objects.all()
    serializer_class = SchoolCoursesSerializer

class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Summary:
        Represents a Model viewset for the School model. Provides read-only operations for School instances.
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Summary:
        Represents a Model viewset for the Course model. Provides read-only operations for Course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

"""
TODO: Implement grade class-based view that extends the ListCreateAPIView, as shown below:

class GradeView(ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
"""
