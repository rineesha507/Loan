"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import sys
import os
from django.core.wsgi import get_wsgi_application

# Print out the Python path to see if it's set correctly
print(sys.path)

# Set the DJANGO_SETTINGS_MODULE directly
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

application = get_wsgi_application()

