FROM jplusplus81/newsblur

COPY      . /srv/newsblur/
COPY      docker/local_settings.py ./local_settings.py