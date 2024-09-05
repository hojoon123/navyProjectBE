from cryptography.fernet import Fernet
from django.contrib.auth import authenticate, login, get_user_model
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.decorators import action

from .models import LoginSession, EncryptionKey, DecryptionKey
from .serializers import UserSerializer

# 현재 프로젝트에서 사용 중인 유저 모델을 가져옵니다.
User = get_user_model()

# 회원가입
class RegisterView(APIView):
    permission_classes = [AllowAny] # 인증 없이 접근 가능
    @transaction.atomic  # 트랜잭션 관리
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()

                # 각 파일에 대한 복호화 키 생성 및 저장
                encryption_keys = EncryptionKey.objects.all()
                for key in encryption_keys:
                    decryption_key = Fernet.generate_key().decode()
                    DecryptionKey.objects.create(
                        user=user,
                        file_name=key.file_name,
                        decryption_key=decryption_key
                    )
                return Response({"message": "회원가입이 성공적으로 완료되었습니다."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            # 중복된 username이나 email로 인한 에러 처리
            transaction.set_rollback(True)  # 트랜잭션 롤백
            return Response({"error": "이미 존재하는 사용자 이름 또는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            # 기타 유효성 검사 에러 처리
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # 기타 예외 처리
            return Response({"error": "서버 에러가 발생했습니다. 잠시 후 다시 시도해 주세요."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# 로그인
class LoginView(APIView):
    permission_classes = [AllowAny]  # 인증 없이 접근 가능
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            current_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')

            # 기존 세션이 존재하는지 확인
            existing_session = LoginSession.objects.filter(user=user, ip_address=current_ip).first()

            if existing_session:
                # 다른 기기면 차단
                if existing_session.user_agent != user_agent:
                    return Response({"error": "동일한 IP에서 다른 장치로 로그인이 시도되었습니다."}, status=status.HTTP_403_FORBIDDEN)

                # IP가 다르면 차단
                if existing_session.ip_address != current_ip:
                    return Response({"error": "다른 IP에서 접속이 시도되었습니다."}, status=status.HTTP_403_FORBIDDEN)

            # 새로운 세션을 저장하거나 기존 세션을 업데이트
            LoginSession.objects.update_or_create(
                user=user,
                ip_address=current_ip,
                defaults={'user_agent': user_agent}
            )
            login(request, user)

            user.last_login = timezone.now()  # 마지막 로그인 시간 업데이트
            user.save()

            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "로그인 성공",
                "access_token": access_token,
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({"error": "잘못된 사용자명 또는 비밀번호입니다."}, status=status.HTTP_400_BAD_REQUEST)

# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # 토큰을 블랙리스트에 추가하여 무효화

            # 로그아웃 시 DB에서 세션 정보 삭제
            LoginSession.objects.filter(user=request.user).delete()

            return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 구독 접근 권한 확인
class HasSubscriptionAccess(BasePermission):
    def has_permission(self, request, view):
        # 사용자가 해당 기능에 접근할 수 있는지 프로필에서 확인
        return request.user.userprofile.has_access_to_feature()

# 특정 서비스 제공 ViewSet - 구독 권한에 따른 그거 설정 돈 낸 사람만 좋은 기능 열어주기 할 떄 이거 걸기
class SomeServiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, HasSubscriptionAccess]  # 인증 및 구독 권한 필요

    @action(detail=False, methods=["get"])
    def some_feature(self, request):
        # 구독 권한을 만족하는 경우에만 접근 가능
        return Response({"message": "Feature accessed successfully!"})


# 유저 구독 플랜 및 프로필 업데이트 뷰
class UpdateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)  # 부분 업데이트 허용

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필이 성공적으로 업데이트되었습니다.", "profile": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)