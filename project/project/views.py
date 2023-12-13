from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

class LoginView(APIView):
    def get(self, request):
        return render(request=request, template_name='app/login.html')
    
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            login(request=request, user=user)
            return Response(data=request.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def get(self, request):
        return render(request=request, template_name='app/logout.html')
    
    def post(self, request):
        logout(request=request)
        return Response(data=request.data, status=status.HTTP_200_OK)
        
class SignupView(APIView):
    def get(self, request):
        return render(request=request, template_name='app/signup.html')
    
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        user = authenticate(username=username, password=password)
        if user:
            return Response(data={'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)