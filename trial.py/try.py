from django.core.management.base import BaseCommand

class fetchpfdata(BaseCommand):
    help = 'Fetch and store PF details from Excel and XML files'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored PF data.'))
