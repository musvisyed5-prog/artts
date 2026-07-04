import os
import sys

# Add the 'src' directory to the python path so that Django can find 'src.settings'
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

import django
django.setup()

from django.conf import settings
from django.core.management import call_command

# Demo mode: when falling back to the /tmp SQLite database (no real DB
# configured), the file starts out empty each cold start, so create the
# schema and static assets before serving any requests.
if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    marker = '/tmp/.demo_initialized'
    if not os.path.exists(marker):
        call_command('migrate', interactive=False, verbosity=0)
        call_command('collectstatic', interactive=False, verbosity=0)
        open(marker, 'w').close()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application
