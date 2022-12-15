# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from .models import User, Todo
from .serializers import UserSerializer, TodoSerializer
from .serializers import ChangePasswordSerializer
import jwt, datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi

from rest_framework import permissions
# Create your views here.


class RegisterView(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect passowrd')
    
        payload = {
            'id':user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token,httponly=True )
        response.data = {
            'jwt':token
        }

        return response
 
class UserView(APIView):
    def get(self, request):
        '''
        Get information about user
        '''
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthentication') 

        try :
            payload = jwt.decode(token,'secret', algorithms=['HS256'])

        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unauthentication') 
        
        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)

class ClientView(APIView):

    def get_object(self,id):
        '''
        Helper method to get the object with given user_id
        '''
        try:
            return User.objects.get(id = id)
        except User.DoesNotExist:
            return None

    def post(self,request):
        '''
        Creating client user
        '''
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthentication') 
        try :
            payload = jwt.decode(token,'secret', algorithms=['HS256'])
            user = User.objects.filter(id=payload['id']).values()[0]
            print(user["role"])

            if user["role"] == "employee" or user["role"] == "admin":
                data = request.data
                if data["role"] != "client":
                    return Response("role should be client") 
                serializer = UserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(serializer.data)
            else:
                raise AuthenticationFailed('unauthertized') 


        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unauthentication') 

    def put(self, request,*args, **kwargs):
        '''
        Updates the client info with given jwt if exists

        '''
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthentication') 

        try :
            payload = jwt.decode(token,'secret', algorithms=['HS256'])

        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unauthentication') 
        print(payload['id'])
        user_instance = self.get_object(payload['id'])
        if not user_instance:
            return Response(
                {"res": "Object with user_id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'email': request.data.get('email'), 
            'password': request.data.get('password'), 
            'id': payload['id']
        }
        serializer = UserSerializer(instance = user_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request,*args, **kwargs):
        '''
        Deletes the client with given jwt if exists
        '''
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthentication') 

        try :
            payload = jwt.decode(token,'secret', algorithms=['HS256'])

        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unauthentication') 
        print(payload['id'])
        todo_instance = self.get_object(payload['id'])
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class EmplyeeView(APIView):
    def get_object(self,id):
        '''
        Helper method to get the object with given user_id
        '''
        try:
            return User.objects.get(id = id)
        except User.DoesNotExist:
            return None
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthentication') 
        try :
            payload = jwt.decode(token,'secret', algorithms=['HS256'])
            user = User.objects.filter(id=payload['id']).values()[0]
            print(user["role"])

            if user["role"] == "admin":
                data = request.data
                if data["role"] != "employee":
                    return Response("role should be employee") 
                serializer = UserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(serializer.data)
            else:
                raise AuthenticationFailed('unauthertized') 


        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unauthentication') 

    def put(self, request,*args, **kwargs):
        '''
        Updates the employee item with given jwt if exists

        '''
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthentication') 

        try :
            payload = jwt.decode(token,'secret', algorithms=['HS256'])

        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unauthentication') 
        print(payload['id'])
        user_instance = self.get_object(payload['id'])
        print(user_instance)
        if not user_instance:
            return Response(
                {"res": "Object with user_id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'email': request.data.get('email'), 
            'password': request.data.get('password'), 
            'id': payload['id']
        }
        serializer = UserSerializer(instance = user_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,*args, **kwargs):
        '''
        Deletes the employee item with given jwt if exists
        '''
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthentication') 

        try :
            payload = jwt.decode(token,'secret', algorithms=['HS256'])

        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unauthentication') 
        print(payload['id'])
        todo_instance = self.get_object(payload['id'])
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK ) 

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Todo.objects.get(id=todo_id, user = user_id)
        except Todo.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, todo_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, todo_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
class LogoutView(APIView):
    def post(self, request):
        response = Response()

        response.delete_cookie('jwt')
        response.data = {
            'message': "sucess"
        }

        return response

class ChangePasswordView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer