from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer


class Login(ObtainAuthToken):
    def post(self, request):
        """
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        """
        login_serializer = self.serializer_class(data=request.data, context={'request': request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(user)
                if created:
                    return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Inicio de sesión exitoso'}, status=status.HTTP_201_CREATED)
                else:
                    """
                    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({'token': token.key, 'user': user_serializer.data, 'message': 'Inicio de sesión exitoso'}, status=status.HTTP_201_CREATED)
                    """
                    token.delete()
                    return Response({'error': 'Ya se ha iniciado sesión con este usuario'}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'error': 'Este usuario no puede iniciar seción'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'mensaje': 'Hola desde response'}, status=status.HTTP_200_OK)

class Logout(APIView):
    def get(self, request):
        try:
            token = request.GET.get('token')
            print(token)
            token = Token.objects.filter(key=token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                session_message = 'Sesiones de usuario eliminadas.'
                token_message = 'Token eliminado'
                return Response({'token_message': token_message, 'session_message': session_message}, status=status.HTTP_200_OK)
            return Response({'error': 'No se ha encontrado un usuario con estas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'No se ha encontrado token en la petición'}, status=status.HTTP_409_CONFLICT)
            

    #def post(self, request):


    
class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Test_token(APIView):
    def get(self, request):
        return Response ({})
    
class UserApiView(APIView):
    def get(self,request):
        users = User.objects.all()
        users_serializer =UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailApiView(APIView):
    def get(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        user.delete()
        return Response({'message': 'usuario eliminado correctamente'}, status=status.HTTP_400_BAD_REQUEST)