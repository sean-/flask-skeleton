-- env PGDATABASE=skeleton PGUSER=pgsql

-- The skeleton_root role should not be able to log in, only users. The root
-- role owns objects and gives "sudo" like access to users with a
-- skeleton_rw_${USER} account.
ALTER ROLE skeleton_root NOLOGIN CONNECTION LIMIT -1;
