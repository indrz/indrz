# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests


from django.contrib.auth.models import User, Group
from django.test import TestCase



def url_ok(url):
    r = requests.head(url)
    return r.status_code == 200



class TranslationRosettaTest(TestCase):

    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testtranslator', password='12345' )
        test_user1.save()

        translator_group = Group.objects.get(name='translators')
        test_user1.groups.add(translator_group)


    # def test_redirect_if_not_logged_in(self):
    #     resp = self.client.get(reverse('admin'))
    #     self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_translator_can_access_rosetta(self):
        login = self.client.login(username='testtranslator', password='12345')
        # resp = self.client.get(reverse('my-borrowed'))
        resp = self.client.get("/rosetta")

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

