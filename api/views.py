import boto3
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from navyProjectBE import settings
from users.models import DecryptionKey

# S3 클라이언트 설정
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME
)


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_name):
        try:
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME  # S3 버킷 이름
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
            file_data = file_obj['Body'].read()

            # 파일 전송 (복호화 없이 그대로 전송)
            response = HttpResponse(file_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response

        except Exception as e:
            return Response({"error": f"파일 다운로드 중 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# 복호화 키 GET API
class GetDecryptionKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_name):
        try:
            # 로그인한 사용자의 특정 파일에 대한 복호화 키 가져오기
            user = request.user
            decryption_key_obj = DecryptionKey.objects.get(user=user, file_name=file_name)
            decryption_key = decryption_key_obj.decryption_key

            return Response({"decryption_key": decryption_key}, status=status.HTTP_200_OK)

        except DecryptionKey.DoesNotExist:
            return Response({"error": "복호화 키가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)