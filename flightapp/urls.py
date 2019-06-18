"""flightapp URL Configuration

"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def home(request):
    return redirect('api-docs')


schema_view = get_schema_view(
    openapi.Info(
        title='Flight Booking API',
        default_version='v1',
        description='An API for booking flights'
    ),
    public=True,
    permission_classes=(permissions.AllowAny, )
)


urlpatterns = [
    path('admin/', admin.site.urls),


    # documentation
    path('api/docs/', schema_view.with_ui('swagger',
                                          cache_timeout=0), name='api-docs'),
    path('', home, name='home'),

    # authentication
    path('api/auth/', include('authentication.urls', namespace='auth')),
]
