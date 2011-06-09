-- env PGDATABASE=template1 PGUSER=pgsql

-- Lots of www processes (use pgbouncer!!!)
CREATE ROLE skeleton_www CONNECTION LIMIT 200 LOGIN;

-- Only one DBA login for now. Once the app goes in to maintenance mode, only
-- use your per-user login. At the end of this procedure the skeleton_dba
-- ROLE is prevented from logging in.
CREATE ROLE skeleton_dba CONNECTION LIMIT 1 LOGIN;

-- There should only ever be one connection as the email user. This limits
-- the possibility of accidentally sending out duplicate emails.
CREATE ROLE skeleton_email CONNECTION LIMIT 1 LOGIN;

-- Note that the skeleton_shadow user can't log in. This is very much
-- intended. The skeleton_shadow user is the user that various functions
-- execute with (think "setuid" privs for certain pl/pgsql functions).
CREATE ROLE skeleton_shadow NOLOGIN;
