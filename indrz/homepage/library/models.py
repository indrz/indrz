# from __future__ import unicode_literals
# from django.utils.encoding import python_2_unicode_compatible
#
# from django.contrib.gis.db import models as gis_models
# from django.utils.translation import  ugettext_lazy as _
#
# from buildings.models import Building, BuildingFloor
#
# @python_2_unicode_compatible
# class Shelf(gis_models.Model):
#     """
#     floor areas as polygons base
#     """
#
#     external_id = gis_models.CharField(verbose_name=_("external_id"), max_length=150, null=True, blank=True)
#     id_letter = gis_models.CharField(verbose_name=_("id shelf letter label"), max_length=150, null=True, blank=True)
#     left_label = gis_models.CharField(verbose_name=_("left label"), max_length=150, null=True, blank=True)
#     righ_label = gis_models.CharField(verbose_name=_("right label"), max_length=150, null=True, blank=True)
#
#     length = gis_models.DecimalField(verbose_name=_("length in m"), max_digits=10, decimal_places=2, null=True, blank=True)
#     length_section = gis_models.DecimalField(verbose_name=_("section lenght in cm"), max_digits=10, decimal_places=2,null=True, blank=True)
#     width = gis_models.DecimalField(verbose_name=_("width in cm of shelf"), max_digits=10, decimal_places=2, null=True, blank=True)
#
#     geom = gis_models.MultiLineStringField(srid=3857, spatial_index=True, null=True, blank=True)
#     objects = gis_models.GeoManager()
#
#     fk_building_floor = gis_models.ForeignKey(BuildingFloor)
#     fk_building = gis_models.ForeignKey(Building)
#
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.short_name or ''