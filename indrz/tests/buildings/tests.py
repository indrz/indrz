# # Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# # This program is free software: you can redistribute it and/or modify
# # it under the terms of the GNU Affero General Public License as
# # published by the Free Software Foundation, either version 3 of the
# # License, or (at your option) any later version.
# #
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# # GNU Affero General Public License for more details.
# #
# # You should have received a copy of the GNU Affero General Public License
# # along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# import sys
# import unittest
#
# from django.core.exceptions import ImproperlyConfigured
# from django.db import ProgrammingError
# from django.utils import six
#
# try:
#     from django.contrib.gis.db.backends.postgis.operations import PostGISOperations
#     HAS_POSTGRES = True
# except ImportError:
#     HAS_POSTGRES = False
# except ImproperlyConfigured as e:
#     # If psycopg is installed but not geos, the import path hits
#     # django.contrib.gis.geometry.backend which will "helpfully" convert
#     # an ImportError into an ImproperlyConfigured.
#     # Here, we make sure we're only catching this specific case and not another
#     # ImproperlyConfigured one.
#     if e.args and e.args[0].startswith('Could not import user-defined GEOMETRY_BACKEND'):
#         HAS_POSTGRES = False
#     else:
#         six.reraise(*sys.exc_info())
#
#
# if HAS_POSTGRES:
#     class FakeConnection(object):
#         def __init__(self):
#             self.settings_dict = {
#                 'NAME': 'test',
#             }
#
#     class FakePostGISOperations(PostGISOperations):
#         def __init__(self, version=None):
#             self.version = version
#             self.connection = FakeConnection()
#
#         def _get_postgis_func(self, func):
#             if func == 'postgis_lib_version':
#                 if self.version is None:
#                     raise ProgrammingError
#                 else:
#                     return self.version
#             elif func == 'version':
#                 pass
#             else:
#                 raise NotImplementedError('This function was not expected to be called')
#
#
# @unittest.skipUnless(HAS_POSTGRES, "The psycopg2 driver is needed for these tests")
# class TestPostgisVersionCheck(unittest.TestCase):
#     """
#     Tests that the postgis version check parses correctly the version numbers
#     """
#
#     def test_get_version(self):
#         expect = '1.0.0'
#         ops = FakePostGISOperations(expect)
#         actual = ops.postgis_lib_version()
#         self.assertEqual(expect, actual)
#
#     def test_version_classic_tuple(self):
#         expect = ('1.2.3', 1, 2, 3)
#         ops = FakePostGISOperations(expect[0])
#         actual = ops.postgis_version_tuple()
#         self.assertEqual(expect, actual)
#
#     def test_version_dev_tuple(self):
#         expect = ('1.2.3dev', 1, 2, 3)
#         ops = FakePostGISOperations(expect[0])
#         actual = ops.postgis_version_tuple()
#         self.assertEqual(expect, actual)
#
#     def test_valid_version_numbers(self):
#         versions = [
#             ('1.3.0', 1, 3, 0),
#             ('2.1.1', 2, 1, 1),
#             ('2.2.0dev', 2, 2, 0),
#         ]
#
#         for version in versions:
#             ops = FakePostGISOperations(version[0])
#             actual = ops.spatial_version
#             self.assertEqual(version[1:], actual)
#
#     def test_invalid_version_numbers(self):
#         versions = ['nope', '123']
#
#         for version in versions:
#             ops = FakePostGISOperations(version)
#             with self.assertRaises(Exception):
#                 ops.spatial_version
#
#     def test_no_version_number(self):
#         ops = FakePostGISOperations()
#         with self.assertRaises(ImproperlyConfigured):
#             ops.spatial_version