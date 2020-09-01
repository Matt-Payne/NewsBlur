FROM haproxy:1.8.22
ENV PYTHONUNBUFFERED=1
WORKDIR   /opt/newsblur
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
COPY . /opt/newsblur/

RUN  python2.7 -m pip install -r requirements.txt --user
COPY local_settings.py.template local_settings.py

RUN python /opt/newsblur/fabfile.py
RUN cp /opt/newsblur/config/haproxy.conf /usr/local/etc/haproxy/haproxy.cfg
RUN 'echo "ENABLED=1" | sudo tee /etc/default/haproxy'
RUN 'cat ${NEWSBLUR_PATH}/config/certificates/newsblur.com.crt > ${NEWSBLUR_PATH}/config/certificates/newsblur.pem'
RUN 'cat ${NEWSBLUR_PATH}/config/certificates/newsblur.com.key >> ${NEWSBLUR_PATH}/config/certificates/newsblur.pem' 
COPY 'config/haproxy_rsyslog.conf' '/etc/rsyslog.d/49-haproxy.conf'
RUN 'restart rsyslog'
RUN 'update-rc.d -f haproxy defaults'

RUN '/etc/init.d/haproxy stop'
RUN 'sleep 5'
CMD '/etc/init.d/haproxy start'