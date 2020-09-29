FROM haproxy:1.8.22
ENV PYTHONUNBUFFERED=1
ENV NEWSBLUR_PATH=/srv/newsblur
WORKDIR   /srv/newsblur
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    python2 \
    cron \
    rsyslog \
    python-setuptools \
    postgresql \
    python-psycopg2 \
    libpq-dev  \
    python-dev  \
    build-essential libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
    python-pip
RUN python -m pip install wheel
#COPY . /opt/newsblur/

#RUN  python2.7 -m pip install -r requirements.txt --user
COPY local_settings.py.template local_settings.py

RUN /bin/bash -c 'echo "ENABLED=1" | tee /etc/default/haproxy'
RUN /bin/bash -c 'mkdir -p /srv/newsblur/config/certificates/'
COPY config/certificates/newsblur.com.pem config/certificates/newsblur.pem
COPY config/certificates/newsblur.com.key config/certificates/newsblur.pem 
COPY 'config/haproxy_rsyslog.conf' '/etc/rsyslog.d/49-haproxy.conf'
#RUN /bin/bash -c 'restart rsyslog'
#RUN /bin/bash -c 'update-rc.d -f haproxy defaults'

#RUN /bin/bash -c '/etc/init.d/haproxy stop'
#RUN /bin/bash -c 'sleep 5'
#CMD /bin/bash -c '/etc/init.d/haproxy start'