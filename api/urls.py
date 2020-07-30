from django.urls import path
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import SchoolViewSet, CourseViewSet, ChangeSchoolViewSet, ChangeCourseViewSet, SchoolCoursesViewSet


router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'changeschools', ChangeSchoolViewSet)
router.register(r'changecourses', ChangeCourseViewSet)
router.register(r'schoolcourses', SchoolCoursesViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns += router.urls