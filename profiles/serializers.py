from dataclasses import fields
from rest_framework import serializers
from .models import Profile


class UserDisplayProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'first_name',
                  'last_name', 'email', 'bio', 'timestamp', 'followers', 'following', 'location']

    def get_username(self, obj):
        return obj.user.username

    def get_followers(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        return obj.user.following.count()

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        return obj.user.last_name


class UserEditProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'location']

    def update(self, instance):
        print(self.validated_data['last_name'])
        instance.user.last_name = self.validated_data['last_name']
        instance.user.first_name = self.validated_data['first_name']
        instance.bio = self.validated_data['bio']
        instance.location = self.validated_data['location']
        instance.user.save()
        instance.save()
        print(instance.location, instance.bio)
        return instance


class UserTestEditProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'location', 'propic']

    def update(self, instance):
        print(self.validated_data['last_name'])
        instance.user.last_name = self.validated_data['last_name']
        instance.user.first_name = self.validated_data['first_name']
        instance.bio = self.validated_data['bio']
        instance.location = self.validated_data['location']
        instance.user.save()
        instance.save()
        print(instance.location, instance.bio)
        return instance
