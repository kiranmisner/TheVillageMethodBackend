"""
Summary:
    Represents the necessary url addresses for the public endpoints of this backend framework. This is primarily
    achieved through the Django REST framework default router class.
"""
from django.urls import path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import SchoolViewSet, CourseViewSet, SchoolCoursesViewSet, CreateUserViewSet

# Initialize and register routes through the default router
router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'schoolcourses', SchoolCoursesViewSet)
router.register(r'createuser', CreateUserViewSet)

# Add token endpoint manually
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

# Add all router-generated urls to urlpatterns
urlpatterns += router.urls
