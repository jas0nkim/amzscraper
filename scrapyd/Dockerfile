#
# scrapyd
#
# inspired by vimagick/scrapyd
# https://github.com/vimagick/dockerfiles/tree/master/scrapyd
# 
# How to:
#
# docker build -t jasonkim/scrapyd:py3.7 .
#
# this image is too bulky (approx. 1.0 GB). need to reduce like vimagick/scrapyd
#

FROM python:3.7-slim

COPY ./requirements.txt /opt/requirements.txt
RUN pip install scrapyd \
    && pip install -r /opt/requirements.txt

COPY ./scrapyd.conf /etc/scrapyd/
VOLUME [ "/etc/scrapyd/", "/var/lib/scrapyd/" ]
EXPOSE 6800

CMD ["scrapyd", "--pidfile="]
