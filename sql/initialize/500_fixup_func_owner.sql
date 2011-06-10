-- env PGDATABASE=skeleton PGUSER=skeleton_root

-- Change the owner of these functions to skeleton_shadow because SECURITY
-- DEFINER is a set attribute for these functions. This must be run as the
-- pgsql user. This can't be run as skeleton_root because skeleton_root isn't
-- a member of the role 'skeleton_shadow' (and shouldn't be!!!).
ALTER FUNCTION aaa.expire_session(TEXT) OWNER TO skeleton_shadow;
ALTER FUNCTION aaa.login(TEXT, BYTEA, INET, TEXT, INTERVAL, BOOL) OWNER TO skeleton_shadow;
ALTER FUNCTION aaa.register(TEXT, BYTEA, INET) OWNER TO skeleton_shadow;
