import time
from django.core.management.base import BaseCommand, CommandError
from market.utils import BusinessRuService


class Command(BaseCommand):
    def handle(self, *args, **options):
        service = BusinessRuService()
        print("Script started succesfuly!")
        while True:
            service.api_client.set_token()
            service.group_to_model()
            service.goods_to_model()
            time.sleep(60 * 5)
