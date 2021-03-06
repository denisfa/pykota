# -*- coding: utf-8 -*-
#
# PyKota : Print Quotas for CUPS
#
# (c) 2003-2013 Jerome Alet <alet@librelogiciel.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# $Id: appinit.py 3561 2013-01-04 22:34:24Z jerome $
#

"""This module exectures some application intialization code."""

import sys
import os
import locale
import gettext

from pykota.utils import initlocale, initgettext

(lang, charset) = initlocale(os.environ.get("PYKOTALANG", ""),
                             os.environ.get("PYKOTACHARSET"))
initgettext(lang, charset)

sys.argv = [a.decode(charset, "replace") for a in sys.argv]
