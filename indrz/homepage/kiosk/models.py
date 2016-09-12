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

from django.contrib.gis.db import models
from buildings.models import Building, Campus


class Kiosk(models.Model):
    name = models.CharField(verbose_name=_('name of kiosk'), max_length= 150, null=True, blank=True)
    ip_address = models.IPAddressField(verbose_name=_('unique IP of the kiosk'), )
    direction_angle = models.IntegerField(verbose_name=_('enter in degrees from 0 to 359 where 0 is north'), help_text="enter the direction a person is facing when standing and looking at the kiosk screen",
                                           null=True, blank=True)
    floor_num = models.IntegerField(verbose_name=_("floor number"), null=True, blank=True)
    building = models.ForeignKey(Building, null=True, blank=True)
    campus = models.ForeignKey(Campus)

    geom = models.PointField(verbose_name=_('location of kiosk'), srid=3857, null=True, blank=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True
        ordering = ['ip_address']

    def __str__(self):
        return str(self.name) or ''
