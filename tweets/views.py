from asyncio.windows_events import NULL
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

from .models import Tweet
from profiles.models import *
from reply.models import *
from notification.models import Notification


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_post_view(request, *args, **kwargs):
    Tweet.objects.create(
        user=request.user,
        content=request.POST['content'],
        image=request.FILES['image'] if request.FILES.get(
            'image') else None
    )
    return Response({}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_repost_view(request, id, *args, **kwargs):
    print(id)
    qs = Tweet.objects.filter(id=id)
    if qs.exists():
        tparent = qs.first()
        Tweet.objects.create(
            user=request.user,
            parent=tparent,
            content=request.POST['content'],
            image=request.FILES['image'] if request.FILES.get(
                'image') else None
        )
        Notification.objects.create(
            tweet=tparent,
            byuser=request.user,
            action="retweet"
        )
    return Response({}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def get_all_tweets_view(request, *args, **kwargs):
    qs = Tweet.objects.all()

    tweetlist = []
    for i in qs:
        userpic = ""
        if (i.user.profile.propic):
            userpic = i.user.profile.propic.url

        pic = ""
        if (i.image):
            pic = i.image.url
        qs = i.tweetreplys.all()
        replylist = []
        for j in qs:
            replylist.append(
                {"by": j.user.username, "message": j.message, "id": j.id, "propic": j.user.profile.propic.url if j.user.profile.propic else ""})
        tweetlist.append({
            "username": i.user.username,
            "userpic": userpic,
            "id": i.id,
            "content": i.content,
            "image": pic,
            "parent_user": i.parent.user.username if i.parent else "",
            "parent_user_image": i.parent.user.profile.propic.url if i.parent and i.parent.user.profile.propic else "",
            "parent_content": i.parent.content if i.parent else "",
            "parent_image": i.parent.image.url if i.parent and i.parent.image else "",
            "retweetscount": Tweet.objects.filter(parent__id=i.id).count(),
            "likes": i.likes.all().count(),
            "iliked": request.user in i.likes.all(),
            "lastmodified": i.timestamp,
            "reply": replylist,
        })
    return Response({"tweetlist": tweetlist}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def get_selected_tweet_view(request, id, *args, **kwargs):
    qs = Tweet.objects.filter(id=id)
    showtweet = {}
    if qs.exists():
        selecttweet = qs.first()

        if selecttweet.user.username == request.user.username:
            userpic = ""
            if (selecttweet.user.profile.propic):
                userpic = selecttweet.user.profile.propic.url

            pic = ""
            if (selecttweet.image):
                pic = selecttweet.image.url
            qs = selecttweet.tweetreplys.all()
            replylist = []
            for j in qs:
                replylist.append(
                    {"by": j.user.username, "message": j.message, "id": j.id, "propic": j.user.profile.propic.url if j.user.profile.propic else ""})
            showtweet = {
                "username": selecttweet.user.username,
                "userpic": userpic,
                "id": selecttweet.id,
                "content": selecttweet.content,
                "image": pic,
                "parent_user": selecttweet.parent.user.username if selecttweet.parent else "",
                "parent_user_image": selecttweet.parent.user.profile.propic.url if selecttweet.parent and selecttweet.parent.user.profile.propic else "",
                "parent_content": selecttweet.parent.content if selecttweet.parent else "",
                "parent_image": selecttweet.parent.image.url if selecttweet.parent and selecttweet.parent.image else "",
                "retweetscount": Tweet.objects.filter(parent__id=selecttweet.id).count(),
                "likes": selecttweet.likes.all().count(),
                "iliked": request.user in selecttweet.likes.all(),
                "lastmodified": selecttweet.timestamp,
                "reply": replylist,
            }
    return Response({"showtweet": showtweet}, status=200)


@ api_view(['GET', 'POST'])
@ permission_classes([IsAuthenticated])
def user_action_view(request, id, *args, **kwargs):
    action = request.data.get("action")
    tweetselected = Tweet.objects.filter(id=id).first()
    if (request.user in tweetselected.likes.all()):
        tweetselected.likes.remove(request.user)
        Notification.objects.create(
            tweet=Tweet.objects.filter(id=id).first(),
            byuser=request.user,
            action="removelike"
        )
    else:
        tweetselected.likes.add(request.user)
        Notification.objects.create(
            tweet=Tweet.objects.filter(id=id).first(),
            byuser=request.user,
            action="like"
        )

    return Response({}, status=200)
