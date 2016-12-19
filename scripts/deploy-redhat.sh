#!/usr/bin/env bash

cd /opt/indrz-wu

rm -rf /opt/django-deploy/indrz
rm -rf /opt/django-deploy/static
rm -rf /opt/django-deploy/media

mkdir /opt/django-deploy/media

# copy source files to destination folder
cp -R /opt/indrz-wu/indrz /opt/django-deploy/indrz


cd /opt/django-deploy/indrz
source /opt/venvs/py3uwsgi/bin/activate
python manage.py collectstatic

cd /opt/indrz-wu/
systemctl restart uwsgi
systemctl reload nginx
