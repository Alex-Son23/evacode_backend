import time

import requests
from django.core.management.base import BaseCommand, CommandError
from market.utils import BusinessRuService


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Script started succesfuly!")
        service = BusinessRuService()
        print("Service created")
        while True:
            service.api_client.set_token()
            service.group_to_model()
            service.goods_to_model()
            print("updated successfully")
            # time.sleep(60 * 5)
            time.sleep(60 * 1)
