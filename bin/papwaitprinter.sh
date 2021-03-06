#! /bin/sh
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
# $Id: papwaitprinter.sh 3561 2013-01-04 22:34:24Z jerome $
#
PATH=$PATH:/bin:/usr/bin:/usr/local/bin:/opt/bin:/sbin:/usr/sbin
sleep 5;
until papstatus -p "$1" | grep -i idle >/dev/null ; do
   sleep 1 ;
done
