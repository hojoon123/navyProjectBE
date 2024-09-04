import json
from django.core.management.base import BaseCommand
from users.models import EncryptionKey


class Command(BaseCommand):
    help = 'JSON 파일에서 암호화 키를 데이터베이스에 로드합니다.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='암호화 키가 포함된 JSON 파일의 경로')

    def handle(self, *args, **options):
        with open(options['json_file'], 'r') as file:
            data = json.load(file)

        for file_name, encryption_key in data.items():
            EncryptionKey.objects.update_or_create(
                file_name=file_name,
                defaults={'encryption_key': encryption_key}
            )
            self.stdout.write(self.style.SUCCESS(f'{file_name}의 키가 성공적으로 추가/업데이트되었습니다.'))
