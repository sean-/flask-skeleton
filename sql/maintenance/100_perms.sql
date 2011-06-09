-- env PGDATABASE=skeleton PGUSER=skeleton_root

-- Update the privileges as you see fit.
-- This script REVOKEs all privs then GRANTs all privs (wrap this in a transaction).

-- The skeleton_root ROLE owns every database object and then GRANTs
-- permissions to the ROLEs skeleton_email, skeleton_shadow and skeleton_www.
-- Individual DBAs log in as their own DBA account, which belongs to the
-- skeleton_dba GROUP. The skeleton_dba GROUP gives visibility, but has
-- severely restricted EXECUTE or "write" privs. Only users in the
-- skeleton_root GROUP have "write" privs. When you want to affect change on
-- the database, you have to change to your skeleton_rw_${USER} account. This
-- is deliberate.

-- Pro tip: Assign object privs to GROUPs and then add user ROLEs to GROUPs.
/*
-- CREATE GROUP skeleton_www;
-- ALTER GROUP skeleton_www ADD USER skeleton_flask;
-- CREATE SCHEMA my_app;
GRANT USAGE ON SCHEMA my_app TO GROUP skeleton_www;
GRANT SELECT ON ALL TABLES IN SCHEMA my_app TO GROUP skeleton_www;
*/


-- BEGIN: Permissions for the 'public' SCHEMA
REVOKE ALL ON SCHEMA public FROM PUBLIC, skeleton_shadow, skeleton_www;
GRANT USAGE ON SCHEMA public TO skeleton_shadow, skeleton_www;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC, skeleton_www;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO skeleton_www;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC, skeleton_www;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO skeleton_www;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC, skeleton_shadow, skeleton_www;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO skeleton_shadow, skeleton_www;
-- END: Permissions for the 'public' SCHEMA


-- BEGIN: Permissions for the 'mod1' SCHEMA
REVOKE ALL ON SCHEMA mod1 FROM PUBLIC, skeleton_www;
GRANT USAGE ON SCHEMA mod1 TO skeleton_www;

REVOKE ALL ON ALL TABLES IN SCHEMA mod1 FROM PUBLIC, skeleton_www;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA mod1 TO skeleton_www;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA mod1 FROM PUBLIC, skeleton_www;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA mod1 TO skeleton_www;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA mod1 FROM PUBLIC, skeleton_www;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA mod1 TO skeleton_www;
-- END: Permissions for the 'mod1' SCHEMA


-- BEGIN: Permissions for the 'aaa' SCHEMA
REVOKE ALL ON SCHEMA aaa FROM PUBLIC, skeleton_www;
GRANT USAGE ON SCHEMA aaa TO skeleton_www;

REVOKE ALL ON ALL TABLES IN SCHEMA aaa FROM PUBLIC, skeleton_www;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA aaa TO skeleton_www;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA aaa FROM PUBLIC, skeleton_www;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA aaa TO skeleton_www;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA aaa FROM PUBLIC, skeleton_www;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA aaa TO skeleton_www;
-- END: Permissions for the 'aaa' SCHEMA


-- BEGIN: Permissions for the 'email' SCHEMA
REVOKE ALL ON SCHEMA email FROM PUBLIC, skeleton_email;
GRANT USAGE ON SCHEMA email TO skeleton_email;

REVOKE ALL ON ALL TABLES IN SCHEMA email FROM PUBLIC, skeleton_email;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA email TO skeleton_email;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA email FROM PUBLIC, skeleton_email;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA email TO skeleton_email;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA email FROM PUBLIC, skeleton_email;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA email TO skeleton_email;
-- END: Permissions for the 'email' SCHEMA


-- BEGIN: Permissions for the 'shadow' SCHEMA.
--
-- Unlike the REVOKE calls above, add more ROLES to the revocation list in
-- order to catch accidental GRANTs.
REVOKE ALL ON SCHEMA shadow FROM PUBLIC, skeleton_email, skeleton_www;
GRANT USAGE ON SCHEMA shadow TO skeleton_shadow;

REVOKE ALL ON ALL TABLES IN SCHEMA shadow FROM PUBLIC, skeleton_email, skeleton_www;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA shadow TO skeleton_shadow;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA shadow FROM PUBLIC, skeleton_email, skeleton_www;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA shadow TO skeleton_shadow;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA shadow FROM PUBLIC, skeleton_email, skeleton_www;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA shadow TO skeleton_shadow;
-- END: Permissions for the 'shadow' SCHEMA




-- Pro tip: use GROUPS instead of ROLES to assign privileges to SCHEMAs.
/*
-- CREATE GROUP www;
-- ALTER GROUP www ADD USER skeleton_www;
-- CREATE SCHEMA www_ro;
GRANT USAGE ON SCHEMA www_ro TO GROUP www;
GRANT SELECT ON ALL TABLES IN SCHEMA www_ro TO GROUP www;
*/
