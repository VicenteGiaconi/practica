from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import LoginView, LogoutView, SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('tokens/', TokenObtainPairView.as_view(), name='tokens'),
    path('login/', csrf_exempt(LoginView.as_view()), name='login'),
    path('logout/', csrf_exempt(LogoutView.as_view()), name='logout'),
    path('signup/', csrf_exempt(SignupView.as_view()), name='signup'),
]
