FROM jmath1/newsblur_base
COPY      docker_local_settings.py docker_local_settings.py
CMD       ["gunicorn", "--bind", ":8000", "wsgi:application"]
