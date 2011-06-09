-- env PGDATABASE=skeleton PGUSER=skeleton_dba

-- Change the owner of these functions to skeleton_shadow because SECURITY
-- DEFINER is a set attribute for these functions. This must be run as the
-- pgsql user (can't be skeleton_dba because skeleton_dba isn't in the role
-- 'skeleton_shadow').
ALTER FUNCTION aaa.expire_session(TEXT) OWNER TO skeleton_shadow;
ALTER FUNCTION aaa.login(TEXT, BYTEA, INET, TEXT, INTERVAL) OWNER TO skeleton_shadow;
ALTER FUNCTION aaa.register(TEXT, BYTEA, INET) OWNER TO skeleton_shadow;
