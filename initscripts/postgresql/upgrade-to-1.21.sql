--
-- PyKota - Print Quotas for CUPS
--
-- (c) 2003-2013 Jerome Alet <alet@librelogiciel.com>
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.
--
-- $Id: upgrade-to-1.21.sql 3561 2013-01-04 22:34:24Z jerome $
--
--
--
-- This script has to be used if you already
-- have a pre-1.21 version of PyKota to upgrade
-- your database schema.
--
-- YOU DON'T NEED TO USE IT IF YOU'VE JUST INSTALLED PYKOTA
--

--
-- Modify the old database schema
--
ALTER TABLE users DROP COLUMN coefficient;
ALTER TABLE users ADD COLUMN overcharge FLOAT;
ALTER TABLE users ALTER COLUMN overcharge SET DEFAULT 1.0;
UPDATE users SET overcharge=1.0;
ALTER TABLE users ALTER COLUMN overcharge SET NOT NULL;

ALTER TABLE userpquota DROP COLUMN warned;
ALTER TABLE userpquota ADD COLUMN warncount INT4;
ALTER TABLE userpquota ALTER COLUMN warncount SET DEFAULT 0;
CREATE INDEX userpquota_u_id_ix ON userpquota (userid);
CREATE INDEX userpquota_p_id_ix ON userpquota (printerid);
UPDATE userpquota SET warncount=0;

CREATE INDEX grouppquota_g_id_ix ON grouppquota (groupid);
CREATE INDEX grouppquota_p_id_ix ON grouppquota (printerid);

ALTER TABLE jobhistory ADD COLUMN md5sum TEXT;
ALTER TABLE jobhistory ADD COLUMN pages TEXT;
ALTER TABLE jobhistory ADD COLUMN billingcode TEXT;
CREATE INDEX jobhistory_u_id_ix ON jobhistory (userid);

--
-- Create the table for coefficients wrt paper sizes and the like
--
CREATE TABLE coefficients (id SERIAL PRIMARY KEY NOT NULL,
                           printerid INTEGER NOT NULL REFERENCES printers(id),
                           label TEXT NOT NULL,
                           coefficient FLOAT DEFAULT 1.0,
                           CONSTRAINT coeffconstraint UNIQUE (printerid, label));

REVOKE ALL ON coefficients FROM public;
REVOKE ALL ON coefficients_id_seq FROM public;
GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON coefficients TO pykotaadmin;
GRANT SELECT, UPDATE ON coefficients_id_seq TO pykotaadmin;
GRANT SELECT ON coefficients TO pykotauser;
