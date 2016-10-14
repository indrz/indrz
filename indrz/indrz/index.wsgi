
import os
import sys
import site

import django
django.setup()

# Add the site-packages of the chosen virtualenv to work with
# site.addsitedir('/opt/.venvs/utc/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/django/utc')
sys.path.append('/var/django/utc/utc_django')

# os.environ['DJANGO_SETTINGS_MODULE'] = 'utc_django.settings'

# Linux server using virtual env
# Activate your virtual env
# activate_env=os.path.expanduser("/opt/.venvs/utc/bin/activate_this.py")
# execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


# windows 2012 server using plain jane python global install
# DJANGO_SETTINGS_MODULE : webgis.settings
# PYTHONPATH : C:\Inetpub\webs\webgis
# WSGI_HANDLER : django.core.wsgi.get_wsgi_application()

