from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LoginSession, UserProfile
from .models import EncryptionKey, DecryptionKey

admin.site.register(EncryptionKey)
admin.site.register(DecryptionKey)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # 기본 UserAdmin 필드셋을 유지하면서 추가 필드를 설정
    fieldsets = (
        *UserAdmin.fieldsets,
        (None, {'fields': ()}),  # 추가 필드가 없으므로 비워둠
    )

    # Admin에서 표시할 필드와 링크로 설정할 필드
    list_display = ('id', 'username', 'email', 'date_joined', 'updated_at', 'is_staff', 'get_subscription_plan')
    list_display_links = ('username',)  # 이 필드를 클릭하여 상세 페이지로 이동할 수 있도록 설정
    search_fields = ('username', 'email')
    ordering = ('id',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # UserProfile의 구독 플랜 정보를 가져오는 메서드 추가
    def get_subscription_plan(self, obj):
        return obj.userprofile.subscription_plan if hasattr(obj, 'userprofile') else "N/A"
    get_subscription_plan.short_description = 'Subscription Plan'


# LoginSession 모델을 별도로 관리할 수 있도록 등록
@admin.register(LoginSession)
class LoginSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'user_agent', 'created_at')
    search_fields = ('user__username', 'ip_address', 'user_agent')
    ordering = ('-created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan')
    search_fields = ('user__username', 'subscription_plan')