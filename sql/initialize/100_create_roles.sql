-- env PGDATABASE=template1 PGUSER=pgsql

-- The skeleton_shadow user can't log in. This is very much intended. The
-- skeleton_shadow user is the user that various functions execute with
-- (think "setuid" privs for certain pl/pgsql functions).
CREATE ROLE skeleton_shadow NOLOGIN;

-- Lots of www processes (use pgbouncer!!!)
CREATE ROLE skeleton_www CONNECTION LIMIT 200 LOGIN;

-- Allow only one connection from skeleton_root user for now. Once the app
-- goes in to maintenance mode, only use your per-user login. At the end of
-- this procedure the skeleton_root ROLE is prevented from logging in. The
-- skeleton_dba ROLE is a read-only GROUP. If a user needs read/write access,
-- they need to use their respective read-write account. Once setup, it's
-- easy to maintain the permissions since you grant permissions to the
-- GROUPs, not to individuals.  Think of it like sudo for dba's.
--
-- "Only you can prevent forrest fires."
CREATE ROLE skeleton_dba NOLOGIN;
CREATE ROLE skeleton_root CONNECTION LIMIT 1 LOGIN IN GROUP skeleton_shadow;

-- There should only ever be one connection as the email user. This limits
-- the possibility of accidentally sending out duplicate emails. The paranoid
-- can use this as a way of preventing duplicate jobs from running and
-- accidentally emailing out duplicates.
CREATE ROLE skeleton_email CONNECTION LIMIT 1 LOGIN;
