from django.shortcuts import render

from rest_framework import viewsets

from .models import School, Course
from .serializers import SchoolSerializer, CourseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

#
#  https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
#

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    # @action(detail=True)
    # def highlight(self, request, *args, **kwargs):
    #     school = self.get_object()
    #     return Response(school.highlighted)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
