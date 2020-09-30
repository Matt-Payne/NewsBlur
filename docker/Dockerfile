FROM newsblur/newsblur
COPY      docker_local_settings.py docker_local_settings.py
CMD       ["gunicorn", "--bind", ":8000", "wsgi:application"]
