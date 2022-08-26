from distutils.log import info
from tweets.models import *
from django.core.files.storage import FileSystemStorage
from http.client import HTTPResponse
import imp
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.http import JsonResponse
# rest import
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from reply.models import *
from tweets.models import *
from .serializers import UserDisplayProfileSerializer, UserEditProfileSerializer, UserTestEditProfileSerializer
# Create your views here.

# Function based views to Class Based Views

from django.contrib.auth.models import User


@api_view(['GET'])
def user_profile_view(request, *args, **kwargs):
    profiles = Profile.objects.all()
    return Response(UserDisplayProfileSerializer(profiles, many=True).data, status=201)


@api_view(['POST', 'GET'])
def user_edit_profile_view(request, *args, **kwargs):
    user = User.objects.filter(username=request.user).first()
    prof = user.profile
    serializer = UserEditProfileSerializer(
        data=request.data, instance=prof)
    if serializer.is_valid(raise_exception=True):
        serializer.update(prof)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def user_test_edit_profile_view(request, *args, **kwargs):
    prof = request.user.profile
    request_file = request.FILES['propic']
    fs = FileSystemStorage()
    file = fs.save(request_file.name, request_file)
    prof.propic = file
    prof.user.first_name = request.POST['first_name']
    prof.user.last_name = request.POST['last_name']
    prof.user.save()
    prof.location = request.POST['location']
    prof.bio = request.POST['bio']
    prof.save()
    print("welcome")
    print(request.FILES.get("propic"))

    return Response({"propic": prof.propic.url}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def profileview(request, name, *args, **kwargs):
    qs = Profile.objects.filter(user__username=name)
    if qs.exists():
        prof = qs.first()
        user = prof.user
        userinfo = {
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email,
            "location": prof.location,
            "bio": prof.bio,
            "ifollow": request.user in prof.followers.all(),
            "propic": prof.propic.url if prof.propic else "",
            "followers": prof.followers.all().count(),
            "following": user.following.all().count()
        }
        owntweets = user.tweets.all()
        tweetlist = []
        for i in owntweets:
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

        return Response({"userinfo": userinfo, "tweetlist": tweetlist}, status=200)
    return Response({}, status=400)


@api_view(['POST', 'GET'])
def likespost(request, name, *args, **kwargs):
    qs = Profile.objects.filter(user__username=name)
    if qs.exists():
        prof = qs.first()
        user = prof.user
        userinfo = {
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email,
            "location": prof.location,
            "bio": prof.bio,
            "ifollow": request.user in prof.followers.all(),
            "propic": prof.propic.url if prof.propic else "",
            "followers": prof.followers.all().count(),
            "following": user.following.all().count()
        }
        owntweets = user.tweet_user.all()
        tweetlist = []
        for i in owntweets:
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

        return Response({"userinfo": userinfo, "tweetlist": tweetlist}, status=200)
    return Response({}, status=400)


@ api_view(['POST', 'GET'])
@ permission_classes([IsAuthenticated])
def replypost(request, name, *args, **kwargs):
    qs = Profile.objects.filter(user__username=name)
    if qs.exists():
        prof = qs.first()
        user = prof.user
        userinfo = {
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email,
            "location": prof.location,
            "bio": prof.bio,
            "ifollow": request.user in prof.followers.all(),
            "propic": prof.propic.url if prof.propic else "",
            "followers": prof.followers.all().count(),
            "following": user.following.all().count()
        }
        replyonpost = user.replys.all()
        tweetlist = []
        for i in replyonpost:
            userpic = ""
            if (i.ontweet.user.profile.propic):
                userpic = i.ontweet.user.profile.propic.url

            pic = ""
            if (i.ontweet.image):
                pic = i.ontweet.image.url
            qs = i.ontweet.tweetreplys.all()
            replylist = []
            for j in qs:
                replylist.append(
                    {"by": j.user.username, "message": j.message, "id": j.id, "propic": j.user.profile.propic.url if j.user.profile.propic else ""})
            tweetlist.append({
                "username": i.ontweet.user.username,
                "userpic": userpic,
                "id": i.ontweet.id,
                "content": i.ontweet.content,
                "image": pic,
                "parent_user": i.ontweet.parent.user.username if i.ontweet.parent else "",
                "parent_user_image": i.ontweet.parent.user.profile.propic.url if i.ontweet.parent and i.ontweet.parent.user.profile.propic else "",
                "parent_content": i.ontweet.parent.content if i.ontweet.parent else "",
                "parent_image": i.ontweet.parent.image.url if i.ontweet.parent and i.ontweet.parent.image else "",
                "retweetscount": Tweet.objects.filter(parent__id=i.ontweet.id).count(),
                "likes": i.ontweet.likes.all().count(),
                "iliked": request.user in i.ontweet.likes.all(),
                "lastmodified": i.ontweet.timestamp,
                "reply": replylist,
            })

        return Response({"userinfo": userinfo, "tweetlist": tweetlist}, status=200)
    return Response({}, status=400)


@ api_view(['POST', 'GET'])
@ permission_classes([IsAuthenticated])
def followerview(request, name, *args, **kwargs):
    qs = Profile.objects.filter(user__username=name)
    if qs.exists():
        prof = qs.first()
        user = prof.user
        followers = prof.followers.all()
        print(followers)
        followerslist = []
        for i in followers:
            followerslist.append(
                {
                    "id": i.id,
                    "username": i.username,
                    "followers": i.profile.followers.count(),
                    "ifollow": request.user in i.profile.followers.all(),
                    "propic": i.profile.propic.url if i.profile.propic else ""
                }
            )
        return Response({"followerslist": followerslist}, status=200)
    return Response({}, status=400)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def followingview(request, name, *args, **kwargs):
    qs = Profile.objects.filter(user__username=name)
    if qs.exists():
        prof = qs.first()
        user = prof.user
        following = user.following.all()
        print(following)
        followinglist = []
        for i in following:
            followinglist.append(
                {
                    "id": i.user.id,
                    "username": i.user.username,
                    "followers": i.followers.count(),
                    "ifollow": request.user in i.followers.all(),
                    "propic": i.propic.url if i.propic else ""
                }
            )
        return Response({"followinglist": followinglist}, status=200)
    return Response({}, status=400)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def exploreview(request, *args, **kwargs):
    qs = Profile.objects.all()
    if qs.exists():
        prof = qs.first()
        user = prof.user
        following = user.following.all()
        userlist = []
        for i in qs:
            if i.user.username != request.user.username:
                userlist.append(
                    {
                        "id": i.user.id,
                        "username": i.user.username,
                        "followers": i.followers.count(),
                        "ifollow": request.user in i.followers.all(),
                        "propic": i.propic.url if i.propic else ""
                    }
                )
        return Response({"userlist": userlist}, status=200)
    return Response({}, status=400)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def followaction(request, name, *args, **kwargs):
    qs = Profile.objects.filter(user__username=name)
    if qs.exists():
        prof = qs.first()
        if (request.user in prof.followers.all()):
            prof.followers.remove(request.user)
        else:
            prof.followers.add(request.user)
        return Response({}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def editprofile(request, name, *args, **kwargs):
    qs = Profile.objects.filter(user__username=name)
    if qs.exists():
        prof = qs.first()
        user = prof.user
        userinfo = {
            "firstname": user.first_name,
            "lastname": user.last_name,
            "location": prof.location,
            "bio": prof.bio
        }
        return Response({"userinfo": userinfo}, status=200)
    return Response({}, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def editprofilewithoutimage(request, *args, **kwargs):
    prof = request.user.profile
    if prof:
        prof.location = request.data.get("location")
        prof.bio = request.data.get("bio")
        prof.user.first_name = request.data.get("firstname")
        prof.user.last_name = request.data.get("lastname")
        prof.user.save()
        prof.save()
        return Response({"msg": "welcome"}, status=200)
    return Response({"msg": "not user"}, status=400)
