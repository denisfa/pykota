#! /usr/bin/python
# -*- coding: utf-8 -*-

# PyKota Print Quota Reports generator
#
# PyKota - Print Quotas for CUPS
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
# $Id: dumpykota.cgi 3561 2013-01-04 22:34:24Z jerome $
#
#

import sys
import os
import cgi
import urllib
from xml.sax import saxutils

import pykota.appinit
from pykota import version, utils
from pykota.dumper import DumPyKota

header = """Content-type: text/html;charset=%s

<html>
  <head>
    <title>%s</title>
    <link rel="stylesheet" type="text/css" href="/pykota.css" />
    <script type="text/javascript">
    <!--
      function checkvalues()
      {
          if ((document.mainform.format.value == "cups") && (document.mainform.datatype.value != "history"))
          {
              alert("Output format and data type are incompatible.");
              return false;
          }

          if (document.mainform.sum.checked && (document.mainform.datatype.value != "payments") && (document.mainform.datatype.value != "history"))
          {
              alert("Summarize is only possible for History and Payments.");
              return false;
          }

          if (document.mainform.sum.checked && (document.mainform.format.value == "cups"))
          {
              alert("Summarize is not possible with CUPS' page_log format.");
              return false;
          }

          return true;
      }
    //-->
    </script>
  </head>
  <body>
    <p>
      <form action="dumpykota.cgi" method="GET" name="mainform" onsubmit="return checkvalues()">
        <table>
          <tr>
            <td>
              <p>
                <a href="%s"><img src="%s?version=%s" alt="PyKota's Logo" /></a>
                <br />
                <a href="%s">PyKota v%s</a>
              </p>
            </td>
            <td colspan="2">
              <h1>%s</h1>
            </td>
          </tr>
          <tr>
            <td colspan="3" align="center">
              <input type="submit" name="report" value="%s" />
            </td>
          </tr>
        </table>
        <p>
          %s
        </p>"""

footer = """
        <table>
          <tr>
            <td colspan="3" align="center">
              <input type="submit" name="report" value="%s" />
            </td>
          </tr>
        </table>
      </form>
    </p>
    <hr width="25%%" />
    <p>
      <font size="-2">
        <a href="http://www.pykota.com/">%s</a>
        &copy; %s %s
        <br />
        <pre>
%s
        </pre>
      </font>
    </p>
  </body>
</html>"""

class PyKotaDumperGUI(DumPyKota) :
    """PyKota Dumper GUI"""
    def guiDisplay(self) :
        """Displays the dumper interface."""
        global header, footer
        content = [ header % (self.charset, _("PyKota Data Dumper"), \
                        self.config.getLogoLink(), \
                        self.config.getLogoURL(), version.__version__, \
                        self.config.getLogoLink(), \
                        version.__version__, _("PyKota Data Dumper"), \
                        _("Dump"), _("Please click on the above button")) ]
        content.append(self.htmlListDataTypes(self.options.data))
        content.append(u"<br />")
        content.append(self.htmlListFormats(self.options.format))
        content.append(u"<br />")
        content.append(self.htmlFilterInput(" ".join(self.arguments)))
        content.append(u"<br />")
        content.append(self.htmlOrderbyInput(self.options.orderby))
        content.append(u"<br />")
        content.append(self.htmlSumCheckbox(self.options.sum))
        content.append(footer % (_("Dump"),
                                 version.__doc__,
                                 version.__years__,
                                 version.__author__,
                                 saxutils.escape(version.__gplblurb__)))
        for c in content :
            sys.stdout.write(c.encode(self.charset, "replace"))
        sys.stdout.flush()

    def htmlListDataTypes(self, selected="") :
        """Displays the datatype selection list."""
        message = '<table><tr><td valign="top">%s :</td><td valign="top"><select name="datatype">' % _("Data Type")
        for dt in self.validdatatypes.items() :
            if dt[0] == selected :
                message += '<option value="%s" selected="selected">%s (%s)</option>' % (dt[0], dt[0], dt[1])
            else :
                message += '<option value="%s">%s (%s)</option>' % (dt[0], dt[0], dt[1])
        message += '</select></td></tr></table>'
        return message

    def htmlListFormats(self, selected="") :
        """Displays the formats selection list."""
        message = '<table><tr><td valign="top">%s :</td><td valign="top"><select name="format">' % _("Output Format")
        for fmt in self.validformats.items() :
            if fmt[0] == selected :
                message += '<option value="%s" selected="selected">%s (%s)</option>' % (fmt[0], fmt[0], fmt[1])
            else :
                message += '<option value="%s">%s (%s)</option>' % (fmt[0], fmt[0], fmt[1])
        message += '</select></td></tr></table>'
        return message

    def htmlFilterInput(self, value="") :
        """Input the optional dump filter."""
        return _("Filter") + (' : <input type="text" name="filter" size="40" value="%s" /> <em>e.g. <strong>username=jerome printername=HP2100 start=today-30</strong></em>' % (value or ""))

    def htmlOrderbyInput(self, value="") :
        """Input the optional ordering."""
        return _("Ordering") + (' : <input type="text" name="orderby" size="40" value="%s" /> <em>e.g. <strong>+username,-printername</strong></em>' % (value or ""))

    def htmlSumCheckbox(self, checked="") :
        """Input the optional Sum option."""
        return _("Summarize") + (' : <input type="checkbox" name="sum" %s /> <em>%s</em>' % ((checked and 'checked="checked"'), _("only for payments or history")))

    def guiAction(self) :
        """Main function"""
        try :
            wantreport = self.form.has_key("report")
        except TypeError :
            pass # WebDAV request probably, seen when trying to open a csv file in OOo
        else :
            if wantreport :
                try :
                    if self.form.has_key("datatype") :
                        self.options.data = self.form["datatype"].value
                    if self.form.has_key("format") :
                        self.options.format = self.form["format"].value
                    if self.form.has_key("filter") :
                        self.arguments = self.form["filter"].value.split()
                    if self.form.has_key("sum") :
                        self.options.sum = self.form["sum"].value
                    if self.form.has_key("orderby") :
                        self.options.orderby = self.form["orderby"].value
                    # when no authentication is done, or when the remote username
                    # is 'root' (even if not run as root of course), then unrestricted
                    # dump is allowed.
                    remuser = os.environ.get("REMOTE_USER", "root")
                    # special hack to accomodate mod_auth_ldap Apache module
                    try :
                        remuser = remuser.split("=")[1].split(",")[0]
                    except IndexError :
                        pass
                    if remuser != "root" :
                        # non-'root' users when the script is password protected
                        # can not dump any data as they like, we restrict them
                        # to their own datas.
                        if self.options.data not in ["printers", "pmembers", "groups", "gpquotas"] :
                            self.arguments.append("username=%s" % remuser)

                    fname = "error"
                    ctype = "text/plain"
                    if self.options.format in ("csv", "ssv") :
                        #ctype = "application/vnd.sun.xml.calc"     # OpenOffice.org
                        ctype = "text/comma-separated-values"
                        fname = "dump.csv"
                    elif self.options.format == "tsv" :
                        #ctype = "application/vnd.sun.xml.calc"     # OpenOffice.org
                        ctype = "text/tab-separated-values"
                        fname = "dump.tsv"
                    elif self.options.format == "xml" :
                        ctype = "text/xml"
                        fname = "dump.xml"
                    elif self.options.format == "cups" :
                        ctype = "text/plain"
                        fname = "page_log"
                    sys.stdout.write("Content-type: %s\n" % ctype)
                    sys.stdout.write("Content-disposition: attachment; filename=%s\n\n" % fname)
                    self.main(self.arguments, self.options, restricted=0)
                except :
                    sys.stdout.write('Content-type: text/html\n\n<html><head><title>CGI Error</title></head><body><p><font color="red">%s</font></p></body></html>\n' % self.crashed("CGI Error").replace("\n", "<br />"))
            else :
                self.guiDisplay()

class FakeCommandLineOptions :
    """A class to fake command line options."""
    output = "-"
    data = "history"
    format = "cups"
    sum = None
    orderby = None

if __name__ == "__main__" :
    utils.reinitcgilocale()
    admin = PyKotaDumperGUI()
    admin.deferredInit()
    admin.form = cgi.FieldStorage()
    admin.options = FakeCommandLineOptions()
    admin.arguments = []
    admin.guiAction()
    try :
        admin.storage.close()
    except (TypeError, NameError, AttributeError) :
        pass

    sys.exit(0)
