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
# $Id: system.py 3561 2013-01-04 22:34:24Z jerome $
#
#

"""This module defines a class for PyKota logging through syslog."""

import sys
import os
import syslog

__revision__ = "$Id: system.py 3561 2013-01-04 22:34:24Z jerome $"

class Logger :
    """A logger class which logs to syslog."""
    levels = { "error" : "ERR", "warn": "WARNING", \
               "info": "INFO", "debug": "DEBUG" }
    def __init__(self) :
        """Opens the logging subsystem."""
        syslog.openlog("PyKota", 0, syslog.LOG_LPR)

    def __del__(self) :
        """Ensures the logging subsystem is closed."""
        syslog.closelog()

    def log_message(self, message, level="info") :
        """Sends the message to syslog."""
        priority = getattr(syslog, \
                           "LOG_%s" % self.levels.get(level.lower(), \
                                                      "DEBUG").upper(), \
                           syslog.LOG_DEBUG)
        try :
            message = message.strip().encode(sys.stdout.encoding or "UTF-8", \
                                             "replace")
        except UnicodeDecodeError :
            pass
        syslog.syslog(priority, "(PID %s) : %s" % (os.getpid(), message))
