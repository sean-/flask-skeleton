-- Lots of www processes (use pgbouncer!!!)
CREATE ROLE skeleton_www CONNECTION LIMIT 200 LOGIN;

-- Only a few admins
CREATE ROLE skeleton_admin CONNECTION LIMIT 2 LOGIN;

-- There should only ever be one connection as the email user. This limits
-- the possibility of accidentally sending out duplicate emails.
CREATE ROLE skeleton_email CONNECTION LIMIT 1 LOGIN;

-- Note that the skeleton_shadow user can't log in. This is very much
-- intended. The skeleton_shadow user is the user that various functions
-- execute with (think "setuid" privs for certain pl/pgsql functions).
CREATE ROLE skeleton_shadow;
