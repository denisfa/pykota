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
-- $Id: upgrade-to-1.23.sql 3561 2013-01-04 22:34:24Z jerome $
--
--
--
-- This script has to be used if you already
-- have a pre-1.23alpha30 version of PyKota to upgrade
-- your database schema.
--
-- YOU DON'T NEED TO USE IT IF YOU'VE JUST INSTALLED PYKOTA
--

--
-- Modify the old database schema
--
ALTER TABLE users ADD COLUMN description TEXT;
ALTER TABLE groups ADD COLUMN description TEXT;
ALTER TABLE userpquota ADD COLUMN maxjobsize INT4;
ALTER TABLE grouppquota ADD COLUMN maxjobsize INT4;
ALTER TABLE printers ADD COLUMN maxjobsize INT4;
ALTER TABLE printers ADD COLUMN passthrough BOOLEAN;
ALTER TABLE printers ALTER COLUMN passthrough SET DEFAULT FALSE;
ALTER TABLE jobhistory ADD COLUMN precomputedjobsize INT4;
ALTER TABLE jobhistory ADD COLUMN precomputedjobprice FLOAT;
ALTER TABLE payments ADD COLUMN description TEXT;

ALTER TABLE userpquota DROP COLUMN temporarydenied;

--
-- Now updates existing datas
--
-- Just to be sure
UPDATE printers SET passthrough=FALSE;

--
-- Create the table for the billing codes
--
CREATE TABLE billingcodes (id SERIAL PRIMARY KEY NOT NULL,
                           label TEXT UNIQUE NOT NULL,
                           description TEXT,
                           balance FLOAT DEFAULT 0.0,
                           pagecounter INT4 DEFAULT 0);
ALTER TABLE billingcodes RENAME COLUMN label TO billingcode;

REVOKE ALL ON billingcodes FROM public;
REVOKE ALL ON billingcodes_id_seq FROM public;
GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON billingcodes TO pykotaadmin;
GRANT SELECT, UPDATE ON billingcodes_id_seq TO pykotaadmin;
GRANT SELECT ON billingcodes TO pykotauser;


