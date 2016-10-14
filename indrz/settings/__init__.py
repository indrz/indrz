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

from __future__ import absolute_import, print_function
import sys


try:
    print("Trying import production_settings.py settings...", file=sys.stderr)
    from .production_settings import *
    print("yes importing production_settings...", file=sys.stderr)
except ImportError:
    print("Trying import common_settings.py ...", file=sys.stderr)
    from .common_settings import *
    print("Now importing common_settings.py settings...", file=sys.stderr)
