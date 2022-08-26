from http.client import HTTPResponse
import imp
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.db import models
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


class Reply(models.Model):
    ontweet = models.ForeignKey(
        Tweet, null=True, blank=True, on_delete=models.SET_NULL, related_name="tweetreplys")
    # many users can many tweets
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="replys")
    message = models.TextField(null=True, blank=True)
