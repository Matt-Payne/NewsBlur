#!/srv/newsblur/venv/newsblur/bin/python

import sys
sys.path.append('/srv/newsblur')

import subprocess
import requests
from newsblur import settings
import socket

def main():
    df = subprocess.Popen(["df", "/"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
    hostname = socket.gethostname()
    percent = int(percent.strip('%'))
    admin_email = settings.ADMINS[0][1]
    
    if percent > 95:
        requests.post(
                "https://api.mailgun.net/v2/%s/messages" % settings.MAILGUN_SERVER_NAME,
                auth=("api", settings.MAILGUN_ACCESS_KEY),
                data={"from": "NewsBlur Disk Monitor: %s <admin@%s.newsblur.com>" % (hostname, hostname),
                      "to": [admin_email],
                      "subject": "%s hit %s%% disk usage!" % (hostname, percent),
                      "text": "Usage on %s: %s" % (hostname, output)})
        print " ---> Disk usage is NOT fine: %s / %s%% used" % (hostname, percent)
    else:
        print " ---> Disk usage is fine: %s / %s%% used" % (hostname, percent)
        
if __name__ == '__main__':
    main()
