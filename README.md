# indrz open source wayfinding, routing, navigation
Project homepage [www.indrz.com] (http://www.indrz.com)
digital wayfinding indoors, maps, orientation and indoor routing for buildings large or small, app or webpage.
[![GitHub stars](https://img.shields.io/github/stars/indrz/indrz.svg?style=flat-square)](https://github.com/indrz/indrz/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/indrz/indrz.svg)](https://github.com/indrz/indrz/issues)
[![GitHub release](https://img.shields.io/github/release/indrz/indrz.svg)](https://github.com/indrz/indrz/releases)
[![license](https://img.shields.io/badge/license-AGPL-blue.svg?style=flat-square)](https://raw.githubusercontent.com/indrz/indrz/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/indrz/indrz.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)


## Licence
indrz is under GNU General Public License v3.0.  The name "indrz" is not allowed to be used by third parties and is a trademark.  Other than that you can do what you want accordingly 


## Documentation

You can find our documentation project here [indrz Docs] (https://github.com/indrz/indrz-doc) in the folder content

Our documentation structure and build environment is built upon the [mapbox docbox] (https://github.com/mapbox/docbox) nodejs static
 documentation generator.  The main content is found under the (content) folder.

[indrz Installation details] (https://github.com/indrz/indrz-doc/blob/master/content/installation.md)

[indrz introduction to API] (https://github.com/indrz/indrz-doc/blob/master/content/introduction.md)

[indrz Directions API] (https://github.com/indrz/indrz-doc/blob/master/content/directions.md)

[indrz Buildings API] (https://github.com/indrz/indrz-doc/blob/master/content/buildings.md)

[indrz Working with GeoData](https://github.com/indrz/indrz-doc/blob/master/content/geodata.md)

## Quick start installation for developers


### Create indrz Ubuntu system user
```bash
adduser indrz
usermod --home /opt/indrz -m indrz #-m moves files too
```
```bash
su indrz
```
if you get a python error on logging into the new user, run:
```bash
dpkg-reconfigure virtualenvwrapper
```

### checkout indrz from github
```bash
cd ~
git clone https://github.com/indrz/indrz.git indrz
cd indrz
git checkout master
```

### Create postgres user

```bash
sudo -u postgres createuser indrz # answer no, no, no
sudo -u postgres createdb indrz -O indrz

```

### Create virtualenv with python 3.4
```bash
cd indrz
mkvirtualenv -p /usr/bin/python3.4 indrz
```
install the requirements using pip.
If you have problems, make sure you have the right version of pip installed
you may need to use pip3
```bash
pip install -r requirements.txt
```
load the demo campus, building, space data
```bash
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py loaddata initial_ltspacetype_data
python manage.py loaddata initial_poi_categories
python manage.py loaddata buildings
```

### Configure your settings

```
cp settings/local.py.example settings/local.py
nano settings/local.py
```

### Start indrz server locally with Django built in server
```
workon indrz
python manage.py runserver
```

### Test if it is running 
```
lynx http://localhost:8000/api/v1/ 
```

## Building blocks Libraries we use

* [Django](http://djangoproject.com) – Web Framework Backend
* [Django Rest Framework](http://www.django-rest-framework.org) – Django Rest Web Framework our API
* [PostGIS](http://postgis.net) – Spatial Database extension to Postgresql
* [PGRouting](http://pgrouting.org) - Routing extension to PostGIS and Posgresql
* [Postgresql](http://www.postgresql.org) – Database
* [Geoserver](http://geoserver.org) – Web map server to serve and create, maps and data
* [Openlayers 3](http://openlayers.org) – Slippy client side javascript mapping library
* [Bootstrap css](http://bootstrap.com/) - css framework bootstrap
* Not YET implemented [Angularjs](http://angularjs.org/) - Javascript framework
* Not YET implemented [three.js](http://threejs.org) - 3d Javascript library
* will be depreciated [jQuery Mobile js](http://http://jquerymobile.com) - mobile web pages made easy
* Not YET implemented [ionic Framework](http://ionicframework.com) - hybrid mobile apps with html 5
* Not YET implemented [Gulpjs js](http://gulpjs.com) - js building 


## Supported and built by:

Contact: Michael Diener

Email: office@gomogi.com

[www.gomogi.com] (http://www.gomogi.com)


