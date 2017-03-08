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

from django.conf.urls import url

from homepage.library.views import rvk_call, book_location, shelf_geom

urlpatterns = [
   url(r'^location/(?P<rvk_id>.+)', book_location, name="book_location"),
   url(r'^shelf/(?P<rvk_id>.+)', shelf_geom, name="shelf geometry"),
   url(r'(?P<rvk_id>.+)', rvk_call, name="call RVK system"),


]


