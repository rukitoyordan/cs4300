import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater_booking.settings")
django.setup()

from django.test import TestCase
from django.test.utils import (
    setup_databases,
    setup_test_environment,
    teardown_databases,
    teardown_test_environment,
)

def before_all(context):
    setup_test_environment()
    context.database_config = setup_databases(verbosity=0, interactive=False)

def before_scenario(context, scenario):
    context.test = TestCase()
    context.test._pre_setup()

def after_scenario(context, scenario):
    context.test._post_teardown()

def after_all(context):
    teardown_databases(context.database_config, verbosity=0)
    teardown_test_environment()
