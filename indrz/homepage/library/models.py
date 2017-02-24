# from django.contrib.gis.db import models as gis_models
# from django.utils.translation import ugettext_lazy as _
# from buildings.models import Building, BuildingFloor
#
#
# class Collection(gis_models.Model):
#     """
#     A set of shelfs that belong together as a collection
#     """
#
#     name = gis_models.CharField(verbose_name=_("Name"), max_length=150, null=True, blank=True)
#
#     def __str__(self):
#         return self.name or ''
#
#
# class Shelf(gis_models.Model):
#     """
#     A bookshelf located on the floor within a building
#     """
#     name = gis_models.CharField(verbose_name=_("Name"), max_length=150, null=True, blank=True)
#     external_id = gis_models.CharField(verbose_name=_("external_id"),
#                                        help_text=_("External ID used by the library to uniquely identify a shelf"),
#                                        max_length=150, null=True, blank=True)
#     id_letter = gis_models.CharField(verbose_name=_("id shelf letter label"), max_length=150, null=True, blank=True)
#
#     section_id = gis_models.CharField(verbose_name=_("Section id"), help_text=_("A section is a small area on a shelf"),
#                                       max_length=150, null=True, blank=True)
#     section_from = gis_models.DecimalField(_("Section start meter value"), decimal_places=2)
#     section_to = gis_models.DecimalField(_("Section start meter value"), decimal_places=2)
#
#     system_from = gis_models.CharField(verbose_name=_("Classification system start range value"), max_length=150,
#                                        null=True, blank=True)
#     system_to = gis_models.CharField(verbose_name=_("Classification system end range value"), max_length=150, null=True,
#                                      blank=True)
#
#     sign_display_from = gis_models.CharField(verbose_name=_("Classification system start range value"), max_length=150,
#                                              null=True, blank=True)
#     sign_disply_to = gis_models.CharField(verbose_name=_("Classification system end range value"), max_length=150,
#                                           null=True, blank=True)
#
#     double_faced = gis_models.BooleanField(_("Does the shelf have two sides"), default=True)
#     vertical_position = gis_models.IntegerField(_("The row position"),
#                                                 help_text=_("The shelf vertical order from bottom 0  to top N"))
#
#     collection = gis_models.CharField(verbose_name=_("Name of collection the shelf belongs to"), null=True, blank=True)
#
#     left_label = gis_models.CharField(verbose_name=_("left label"),
#                                       help_text=_("Map left label range shown on the 2d map"), max_length=150,
#                                       null=True, blank=True)
#     righ_label = gis_models.CharField(verbose_name=_("right label"),
#                                       help_text=_("Map right label range shown on the 2d map"), max_length=150,
#                                       null=True, blank=True)
#
#     length = gis_models.DecimalField(verbose_name=_("length in m"), max_digits=10, decimal_places=2, null=True,
#                                      blank=True)
#     length_section = gis_models.DecimalField(verbose_name=_("section lenght in cm"), max_digits=10, decimal_places=2,
#                                              null=True, blank=True)
#
#     width = gis_models.DecimalField(verbose_name=_("width in cm of shelf"), max_digits=10, decimal_places=2, null=True,
#                                     blank=True)
#     depth = gis_models.DecimalField(verbose_name=_("depth in cm of shelf"), max_digits=10, decimal_places=2, null=True,
#                                     blank=True)
#
#     fk_building_floor = gis_models.ForeignKey(BuildingFloor)
#     fk_building = gis_models.ForeignKey(Building)
#
#     def start_label(self):
#         """
#         Assumes the user would be looking down the shelf
#         geometry from Linestring StartPoint to EndPoint
#
#         Generates the label for the start side of the shelf
#         including the classification system from  and to value
#
#         Return the START From-To label from the right side and
#         Return the START From-To label from the left side
#         :return:
#         """
#         pass
#
#     def end_label(self):
#         """
#         Assumes the user would be looking down the shelf
#         geometry from Linestring EndPoint to StartPoint
#
#         Generates the label for the end side of the shelf
#         including the classification system from  and to value
#
#         Return the END From-To label from the right side and
#         Return the END From-To label from the left side
#         :return:
#         """
#         #
#
#         pass
#
#     def __str__(self):
#         return self.name or ''
#
#
# class ShelfGeometry(gis_models.Model):
#     """
#     The geometry line of a shelfs actual location on floor within a building
#     """
#     shelf = gis_models.ForeignKey(Shelf, null=True, blank=True)
#
#     objects = gis_models.GeoManager()
#
#     fk_building_floor = gis_models.ForeignKey(BuildingFloor)
#     fk_building = gis_models.ForeignKey(Building)
#
#     def start_point(self):
#         pass
#
#     def end_point(self):
#         pass
#
#     def left_side(self):
#         pass
#
#     def right_side(self):
#         pass
#
#     def left_label(self):
#         pass
#
#     def right_label(self):
#         pass
#
#     def __str__(self):
#         return self.name or ''
