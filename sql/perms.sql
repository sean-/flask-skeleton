-- Update the privileges as you see fit.
-- This script REVOKEs all privs then GRANTs all privs (wrap this in a transaction).

-- BEGIN: Permissions for the 'public' SCHEMA
REVOKE ALL ON SCHEMA public FROM skeleton_www;
GRANT USAGE ON SCHEMA public TO skeleton_www;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM skeleton_www;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO skeleton_www;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM skeleton_www;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO skeleton_www;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM skeleton_www;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO skeleton_www;
-- END: Permissions for the 'public' SCHEMA

-- BEGIN: Permissions for the 'mod1' SCHEMA
REVOKE ALL ON SCHEMA mod1 FROM skeleton_www;
GRANT USAGE ON SCHEMA mod1 TO skeleton_www;

REVOKE ALL ON ALL TABLES IN SCHEMA mod1 FROM skeleton_www;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA mod1 TO skeleton_www;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA mod1 FROM skeleton_www;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA mod1 TO skeleton_www;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA mod1 FROM skeleton_www;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA mod1 TO skeleton_www;
-- END: Permissions for the 'mod1' SCHEMA


-- Pro tip: put different database objects in different schemas so that you can
-- assign different privileges to different schemas in a blanket way. For
-- example: add a schema that is read-only for the web group.
/*
-- CREATE GROUP www;
-- ALTER GROUP www ADD USER www;
-- CREATE SCHEMA www_ro;
GRANT USAGE ON SCHEMA www_ro TO GROUP www;
GRANT SELECT ON ALL TABLES IN SCHEMA www_ro TO GROUP www;
*/

-- Using the SECURITY DEFINER option for functions is a neat way to provide "setuid" functions that do update "read-only" tables.
