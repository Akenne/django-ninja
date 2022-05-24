from django.core.management import BaseCommand
from api.models import Loss
import json

class Command(BaseCommand):
    help = 'Load a json loss file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        f = open(path)
        data = json.load(f)
        for d in data:
            Loss.objects.create(
                company_id = d['company_id'],
                company_name = d['company_name'],
                scenario = int(d['scenario']),
                total = d['total'],
                hurricane = d['hurricane'],
                flood = d['flood'],
                storm = d['storm'],
                wildfire = d['wildfire'],
            )
            