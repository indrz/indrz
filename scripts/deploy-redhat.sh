rm -rf /opt/deploy-django/indrz
rm -rf /opt/deploy-django/static
rm -rf /opt/deploy-django/media

mkdir /opt/deploy-django/media

# copy source files to destination folder
cp -R /opt/indrz-wu/indrz /opt/django-deploy/indrz


cd /opt/indrz-wu/indrz
python manage.py collectstatic
