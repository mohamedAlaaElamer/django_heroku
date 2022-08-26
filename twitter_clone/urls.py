"""twitter_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from accounts.views import *
from profiles.views import *
from reply.views import create_reply_view
from tweets.views import *
from chatmessages.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('register/', register_view),
    path('logout/', logout_view),
    path('', home_view),
    # rest api views
    # registeration views
    path('createuser/', user_create_view),
    path('getallusers/', user_diplay_view),
    path('userlogin/', user_login_view),
    path('userlogout/', user_logout_view),
    # profiles views
    path('userprofile/', user_profile_view),
    path('usereditprofile/', user_edit_profile_view),
    # authenication token generators
    path('api/', include('accounts.api.urls')),
    path('editprofile/', user_test_edit_profile_view),
    path('creattweet/', create_post_view),
    path('creatretweet/<int:id>', create_repost_view),
    path('getalltweets/', get_all_tweets_view),
    path('createreply/<int:id>', create_reply_view),
    path('tweetaction/<int:id>', user_action_view),
    path('userinfo/', user_info_view),
    path('newuserprofile/<name>', profileview),
    path('like/<name>', likespost),
    path('reply/<name>', replypost),
    path('follow/<name>', followaction),
    path('follower/<name>', followerview),
    path('following/<name>', followingview),
    path('explore/', exploreview),
    path('editprofileinfo/<name>', editprofile),
    path('withoutimage/', editprofilewithoutimage),
    # chat views
    path('sendmessageto/<name>', sendmessage),
    path('divmessages/<name>', getusermessage),
    path('getallmessages/', getallmessages),
    path('gettweetbyid/<int:id>', get_selected_tweet_view)


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
