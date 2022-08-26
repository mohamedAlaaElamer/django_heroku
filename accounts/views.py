from http.client import HTTPResponse
import imp
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# rest import
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserDisplaySerializer
# Create your views here.

# Function based views to Class Based Views
from django.contrib.auth.models import User
from profiles.models import *

def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("/")
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context = {
        "form": form,
        "btn_label": "Login",
        "title": "Login"
    }
    return render(request, "accounts/auth.html", context)


def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Click to Confirm",
        "title": "Logout"
    }
    return render(request, "accounts/auth.html", context)


def register_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("/")
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        # send a confirmation email to verify their account
        login(request, user)
        return redirect("/")
    context = {
        "form": form,
        "btn_label": "Register",
        "title": "Register"
    }
    return render(request, "accounts/auth.html", context)


def home_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login")
    return render(request, "accounts/home.html")


@api_view(['POST', 'GET'])
def user_create_view(request, *args, **kwargs):
    print(request.data)
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_diplay_view(request, *args, **kwargs):
    users = User.objects.all()
    return Response(UserDisplaySerializer(users, many=True).data, status=201)


@api_view(['GET', 'POST'])
def user_login_view(request, *args, **kwargs):
    username = request.data.get("username")
    password = request.data.get("password")
    print(username, password)
    user = authenticate(request=request,
                        username=username, password=password)
    if user:
        login(request, user)
        return Response({"msg": "welcome"}, status=201)
    return Response({"msg": "not user"}, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_logout_view(request, *args, **kwargs):
    logout(request)
    return Response({"msg": "done"}, status=201)




# user info return username and image
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_info_view(request, *args, **kwargs):
    if request.user:
        userinfo ={
            "username":request.user.username,
            "propic":request.user.profile.propic.url if request.user.profile.propic else ""
        }
        return Response(userinfo,status=200)
    return Response({"message":"unuser"},status=400)
