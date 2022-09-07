import imp
from urllib import response
from django.shortcuts import render
from .models import Chatmessage
from django.contrib.auth.models import User
# rest import
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Q
from profiles.models import Profile
from notification.models import Notification
# Create your views here.


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def getallmessages(request, *args, **kwargs):
    qs = Chatmessage.objects.filter(touser=request.user)
    qnot = Notification.objects.filter(Q(tweet__user=request.user) | Q(foruser=request.user))
    messagelist = []
    notlist = []
    if qs.exists():
        for i in qs:
            messagelist.append({
                "from": i.formuser.username,
                "propic": i.formuser.profile.propic.url if i.formuser.profile.propic else "",
                "to": i.touser.username,
                "message": i.message
            })

    if qnot.exists():
        for i in qnot:
            notlist.append({
                "username": i.byuser.username,
                "propic": i.byuser.profile.propic.url if i.byuser.profile.propic else "",
                "action": i.action,
                "id": i.tweet.id if i.tweet else "",
            }
            )
    return Response({"message": messagelist, "notlist": notlist}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def getusermessage(request, name, *args, **kwargs):
    qs = Chatmessage.objects.filter(
        Q(touser=request.user, formuser__username=name) | Q(touser__username=name, formuser=request.user))
    another = User.objects.filter(username=name).first()
    if qs.exists():
        messagelist = []
        for i in qs:
            messagelist.append({
                "from": i.formuser.username,
                "to": i.touser.username,
                "message": i.message,

            })
        return Response({"message": messagelist, "propic": another.profile.propic.url if another.profile.propic else ""}, status=200)
    return Response({"message": [], "propic": another.profile.propic.url if another.profile.propic else ""}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def sendmessage(request, name, *args, **kwargs):
    tothat = User.objects.filter(username=name).first()
    mes = Chatmessage.objects.create(
        touser=tothat,
        formuser=request.user,
        message=request.POST['content']
    )
    if mes:
        return Response({"message": "sent"}, status=200)
    return Response({"message": "error"}, status=400)
