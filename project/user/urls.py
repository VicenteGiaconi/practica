from django.urls import path
from .views import Login, Signup, Test_token, UserApiView, UserDetailApiView, Logout

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('test_token/', Test_token.as_view(), name='test_token'),
    path('user_view/', UserApiView.as_view(), name='user_view'),
    path('user_detail_view/<int:pk>/', UserDetailApiView.as_view(), name='user_deail_view'),
    path('logout/', Logout.as_view(), name='logut'),
]