-- The dba role should not be able to log in, only users. The dba role owns
-- objects, that's it.
ALTER ROLE skeleton_dba NOLOGIN CONNECTION LIMIT -1;
