from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
]
