FROM jmath1/newsblur_base
#COPY      . /opt/newsblur/
#COPY      docker/local_settings.py ./local_settings.py
CMD       ["gunicorn", "--bind", ":8000", "wsgi:application"]
