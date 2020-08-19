"""
WSGI config for myproject project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

if os.getenv("DOCKERBUILD"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()