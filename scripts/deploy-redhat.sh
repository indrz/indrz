rm -rf /opt/deploy-django/indrz
rm -rf /opt/deploy-django/static
rm -rf /opt/deploy-django/media

mkdir /opt/deploy-django/media

# copy source files to destination folder
cp -R /opt/indrz-wu/indrz /opt/django-deploy/indrz


cd /opt/deploy-django/indrz
source /opt/venvs/py3uwsgi/bin/activate
python manage.py collectstatic

systemctl stop uwsgi
systemctl start uwsgi
systemctl reload nginx
