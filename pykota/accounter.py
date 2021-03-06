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
# $Id: accounter.py 3561 2013-01-04 22:34:24Z jerome $
#
#

"""This module defines base classes used by all accounting methods."""

import sys
import os
import imp

from pykota.errors import PyKotaAccounterError

class AccounterBase :
    """A class to account print usage by querying printers."""
    def __init__(self, kotafilter, arguments, ispreaccounter=0, name="Unknown") :
        """Sets instance vars depending on the current printer."""
        self.name = name
        self.filter = kotafilter
        self.arguments = arguments
        self.onerror = self.filter.config.getPrinterOnAccounterError(self.filter.PrinterName)
        self.isSoftware = 1 # by default software accounting
        self.isPreAccounter = ispreaccounter
        self.inkUsage = []

    def getLastPageCounter(self) :
        """Returns last internal page counter value (possibly faked)."""
        try :
            return self.LastPageCounter or 0
        except :
            return 0

    def beginJob(self, printer) :
        """Saves the computed job size."""
        # computes job's size
        self.JobSize = self.computeJobSize()

        # get last job information for this printer
        if not self.isPreAccounter :
            # TODO : check if this code is still needed
            if not printer.LastJob.Exists :
                # The printer hasn't been used yet, from PyKota's point of view
                self.LastPageCounter = 0
            else :
                # get last job size and page counter from Quota Storage
                # Last lifetime page counter before actual job is
                # last page counter + last job size
                self.LastPageCounter = int(printer.LastJob.PrinterPageCounter or 0) + int(printer.LastJob.JobSize or 0)

    def fakeBeginJob(self) :
        """Do nothing."""
        pass

    def endJob(self, printer) :
        """Do nothing."""
        pass

    def getJobSize(self, printer) :
        """Returns the actual job size."""
        try :
            return self.JobSize
        except AttributeError :
            return 0

    def computeJobSize(self) :
        """Must be overriden in children classes."""
        raise RuntimeError, "AccounterBase.computeJobSize() must be overriden !"

def openAccounter(kotafilter, ispreaccounter=0) :
    """Returns a connection handle to the appropriate accounter."""
    if ispreaccounter :
        (backend, args) = kotafilter.config.getPreAccounterBackend(kotafilter.PrinterName)
    else :
        (backend, args) = kotafilter.config.getAccounterBackend(kotafilter.PrinterName)
    try :
        accounterbackend = imp.load_source("accounterbackend",
                                            os.path.join(os.path.dirname(__file__),
                                                         "accounters",
                                                         "%s.py" % backend.lower()))
    except ImportError :
        raise PyKotaAccounterError, _("Unsupported accounter backend %s") % backend
    else :
        return accounterbackend.Accounter(kotafilter, args, ispreaccounter, backend.lower())
