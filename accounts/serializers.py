from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import login, logout, authenticate


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'password1']
        extra_kwargs = {'password': {'write_only': True}}

    # email must be unique and valide
    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if not value or qs.exists():
            raise serializers.ValidationError("must enter uniqu email")
        return value

    def validate(self, data):
        if data['password1'] != data['password']:
            raise serializers.ValidationError("must enter same password")
        return data

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'])

        user.set_password(self.validated_data['password'])

        user.save()
        return user


class UserDisplaySerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'followers', 'bio']

    def get_followers(self, obj):
        return obj.profile.followers.count()

    def get_bio(self, obj):
        return obj.profile.bio
