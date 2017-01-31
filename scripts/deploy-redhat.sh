#!/usr/bin/env bash

cd /opt/indrz-wu

# copy all server made translation changes to temp dir
rm -rf /home/mdiener/temp/de

cp -R /opt/django-deploy/indrz/locale/de /home/mdiener/temp/

rm -rf /opt/django-deploy/indrz
rm -rf /opt/django-deploy/static
rm -rf /opt/django-deploy/media

mkdir /opt/django-deploy/media

# copy source files to destination folder
cp -R /opt/indrz-wu/indrz /opt/django-deploy/indrz

# restore server made translations after deploy
rm -rf /opt/django-deploy/indrz/locale/de
cp -R /home/mdiener/temp/de /opt/django-deploy/indrz/locale/de


cd /opt/django-deploy/indrz
source /opt/venvs/py3uwsgi/bin/activate
python manage.py collectstatic --clear

cd /opt/indrz-wu/
supervisorctl reload
systemctl reload nginx
