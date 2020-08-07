from django.shortcuts import render
from django.contrib.auth import get_user_model 

from rest_framework import viewsets

from .models import School, Course, Grade, CustomUser
from .serializers import SchoolSerializer, CourseSerializer, SchoolCoursesSerializer, GradeSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListCreateAPIView

#
#  https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
#

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = CustomUser.objects.all()
    # serializer_class = UserSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAdminUser]

class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class SchoolCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolCoursesSerializer

class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ChangeSchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

class ChangeCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

class GradeView(ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)