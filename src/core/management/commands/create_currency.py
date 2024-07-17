from django.core.management import BaseCommand

from core.models import Currency


class Command(BaseCommand):

    def handle(self, *args, **options):
        Currency.objects.get_or_create(name='Воны - Рубли - Тенге', key='krw-rub-kzt', value=12.0)
        Currency.objects.get_or_create(name='Воны - Рубли - Евро', key='krw-rub-eur', value=13.0)
        self.stdout.write(self.style.SUCCESS('Successfully created exchange rates'))