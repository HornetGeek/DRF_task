from django.urls import path, include
from django.contrib import admin
from .views import *
urlpatterns = [
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('client', ClientView.as_view()),
    path('employee', EmplyeeView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('todo', TodoListApiView.as_view()),
    path('todo/<int:todo_id>/', TodoDetailApiView.as_view()),

]
