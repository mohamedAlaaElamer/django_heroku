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


# Create your views here.

# Function based views to Class Based Views
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from tweets.models import Tweet
from reply.models import *
from notification.models import Notification


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_reply_view(request, id, *args, **kwargs):
    Reply.objects.create(
        ontweet=Tweet.objects.filter(id=id).first(),
        user=request.user,
        message=request.POST['message'])
    Notification.objects.create(
        tweet=Tweet.objects.filter(id=id).first(),
        byuser=request.user,
        action="reply"
    )
    print("hasbeen tested")
    return Response({}, status=200)
