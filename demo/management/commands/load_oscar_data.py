import os

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    """
    Import Oscar fixtures
    """
    def handle_noargs(self, **options):
        fixtures_dir = os.path.join(settings.PROJECT_ROOT, 'demo', 'fixtures')
        catalogue_dir = os.path.join(fixtures_dir, 'catalogue')

        products_file = os.path.join(catalogue_dir, 'child_products.json')
        orders_file = os.path.join(catalogue_dir, 'orders.json')
        image_src = os.path.join(catalogue_dir, 'images.tar.gz')

        csv_files = [
            os.path.join(catalogue_dir, 'books.computers-in-fiction.csv'),
            os.path.join(catalogue_dir, 'books.essential.csv'),
            os.path.join(catalogue_dir, 'books.hacking.csv'),
        ]

        json_files = [
            os.path.join(fixtures_dir, 'pages.json'),
            os.path.join(fixtures_dir, 'auth.json'),
            os.path.join(fixtures_dir, 'ranges.json'),
            os.path.join(fixtures_dir, 'offers.json'),
        ]

        call_command('loaddata', products_file, verbosity=0)
        call_command('oscar_import_catalogue', *csv_files, verbosity=0)
        call_command('oscar_import_catalogue_images', image_src, verbosity=0)
        call_command('oscar_populate_countries', verbosity=0)
        call_command('loaddata', *json_files, verbosity=0)
        call_command('loaddata', orders_file, verbosity=0)
