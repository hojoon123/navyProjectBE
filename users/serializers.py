from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction

from .models import CustomUser
from rest_framework import serializers
from .models import UserProfile, SubscriptionPlan

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["subscription_plan"]

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id", "first_name", "last_name", "username",
            "email", "password", "userprofile",
            "date_joined", "updated_at", "last_login"
        ]

    def validate(self, data):
        # 중복 체크 로직 추가
        if CustomUser.objects.filter(username=data.get('username')).exists():
            raise ValidationError("이미 존재하는 사용자 이름입니다.")
        if CustomUser.objects.filter(email=data.get('email')).exists():
            raise ValidationError("이미 존재하는 이메일입니다.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop("userprofile", {})
        password = validated_data.pop('password')

        # 사용자 생성
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("userprofile", {})
        subscription_plan = profile_data.get("subscription_plan")

        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        # Update UserProfile
        profile = instance.userprofile
        if subscription_plan:
            profile.subscription_plan = subscription_plan
        profile.save()

        return instance
