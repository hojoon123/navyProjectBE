from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class EncryptionKey(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    encryption_key = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name

class DecryptionKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='decryption_keys')
    file_name = models.CharField(max_length=255)
    decryption_key = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.file_name}"

class CustomUser(AbstractUser):
    # 필드 추가
    username = models.CharField(max_length=150, unique=True)
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트일

    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class SubscriptionPlan(models.TextChoices):
    FREE = "FREE", "Free Plan"
    BASIC = "BASIC", "Basic Plan"
    PRO = "PRO", "Pro Plan"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userprofile"
    )
    subscription_plan = models.CharField(
        max_length=10,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.FREE,
    )

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan}"

    def has_access_to_feature(self):
        """사용자가 구독 플랜에 따라 특정 기능에 접근할 수 있는지 확인하세요"""
        return self.subscription_plan != SubscriptionPlan.FREE

class LoginSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()  # IP 주소
    user_agent = models.CharField(max_length=255)  # User-Agent 정보
    created_at = models.DateTimeField(auto_now_add=True)  # 로그인 시간

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.user_agent}"