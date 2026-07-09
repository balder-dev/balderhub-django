import os
import logging
from django.contrib.auth import get_user_model
import balder
from balderplugin.junit import JunitPlugin

import django

django.setup()

from book.models import Author, Book, Category

logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.DEBUG)

logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


@balder.fixture(level='session')
def create_superuser():
    # this command is using the os environment variables (`DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`)
    User = get_user_model()

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    if not User.objects.filter(username=username).exists():
        logger.info(f'create new username `{username}`')
        from django.core.management import execute_from_command_line
        execute_from_command_line(['balderglob.py', 'createsuperuser', '--noinput'])
    else:
        logger.info(f'superuser with username `{username}` already exists - do nothing')


def _clean_database():
    Book.objects.all().delete()
    Author.objects.all().delete()
    Category.objects.all().delete()

@balder.fixture(level='session')
def clean_database():
    _clean_database()

@balder.fixture(level='testcase')
def load_django_fixtures():
    logger.info('load django fixtures')
    from django.core.management import execute_from_command_line
    execute_from_command_line(['balderglob.py', 'loaddata',
                               'authors', 'categories','books'])
    yield
    logger.info('delete all data from database')
    _clean_database()