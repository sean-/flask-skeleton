-- module home's models
CREATE TABLE public.h1 (
       id SERIAL,
       val TEXT,
       PRIMARY KEY(id)
);

CREATE TABLE public.h2 (
       id SERIAL,
       val TEXT,
       val2 TEXT,
       PRIMARY KEY(id)
);

-- module mod1's models
CREATE SCHEMA mod1;
CREATE TABLE mod1.h1 (
       id SERIAL,
       val2 TEXT,
       PRIMARY KEY(id)
);

-- module mod3's models
CREATE TABLE public.page (
       id SERIAL,
       url TEXT,
       PRIMARY KEY(id)
);
CREATE UNIQUE INDEX page_url_udx ON public.page(LOWER(url));

CREATE TABLE public.tag (
       id SERIAL,
       name TEXT,
       PRIMARY KEY(id)
);
CREATE UNIQUE INDEX tag_name_udx ON public.tag(LOWER(name));

CREATE TABLE public.page_tags (
       page_id INT NOT NULL,
       tag_id INT NOT NULL,
       PRIMARY KEY(page_id, tag_id),
       FOREIGN KEY(page_id) REFERENCES public.page(id),
       FOREIGN KEY(tag_id) REFERENCES public.tag(id)
);
CREATE UNIQUE INDEX page_tags_tag_page_id_udx ON public.page_tags (tag_id, page_id);


-- BEGIN: aaa's database objects
CREATE SCHEMA aaa;
CREATE SCHEMA shadow;

CREATE TABLE shadow.aaa_email (
       id SERIAL,
       email TEXT NOT NULL,
       user_id INT NOT NULL,
       PRIMARY KEY(id)
);
CREATE UNIQUE INDEX email_email_lower_udx ON shadow.aaa_email(LOWER(email));

CREATE TABLE shadow.aaa_email_confirmation_log (
       email_id INT NOT NULL,
       timestamp_sent TIMESTAMP WITH TIME ZONE NOT NULL,
       ttl INTERVAL NOT NULL DEFAULT '8 hours'::INTERVAL,
       confirmation_code TEXT NOT NULL,
       confirmed BOOL NOT NULL DEFAULT FALSE,
       ip_address INET,
       timestamp_confirmed TIMESTAMP WITH TIME ZONE,
       CHECK (confirmed = FALSE OR (confirmed = TRUE AND ip_address IS NOT NULL AND timestamp_confirmed IS NOT NULL)),
       FOREIGN KEY(email_id) REFERENCES shadow.aaa_email(id)
);
CREATE INDEX aaa_email_confirmation_log_email_idx ON shadow.aaa_email_confirmation_log(email_id);

CREATE TABLE shadow.aaa_user (
       id SERIAL,
       hashpass TEXT NOT NULL,
       active BOOL NOT NULL DEFAULT FALSE,
       primary_email_id INT NOT NULL,
       registration_utc TIMESTAMP WITH TIME ZONE NOT NULL,
       registration_ip INET NOT NULL,
       PRIMARY KEY(id),
       FOREIGN KEY(primary_email_id) REFERENCES shadow.aaa_email(id)
);
CREATE UNIQUE INDEX aaa_user_primary_email_udx ON shadow.aaa_user(primary_email_id);
ALTER TABLE shadow.aaa_email ADD CONSTRAINT email_user_fk FOREIGN KEY(user_id) REFERENCES shadow.aaa_user(id) INITIALLY DEFERRED;

CREATE TABLE shadow.aaa_login_attempts (
       id SERIAL,
       user_id INT NOT NULL,
       login_utc TIMESTAMP WITH TIME ZONE NOT NULL,
       logout_utc TIMESTAMP WITH TIME ZONE,
       ip_address INET NOT NULL,
       success BOOL NOT NULL,
       notes TEXT,
       PRIMARY KEY(id),
       FOREIGN KEY(user_id) REFERENCES shadow.aaa_user(id),
       CHECK (success OR (NOT success AND notes IS NOT NULL))
);
CREATE INDEX aaa_login_attempts_user_login_idx ON shadow.aaa_login_attempts(user_id, login_utc);

-- Torn on whether or not to show this view since access to this data should
-- only be done via functions
CREATE VIEW aaa.email (id, email, user_id) AS
	SELECT
		e.id, e.email, e.user_id
	FROM
		shadow.aaa_email AS e, shadow.aaa_email_confirmation_log AS ecl
	WHERE
		e.id = ecl.email_id AND ecl.confirmed = TRUE;

-- Only show active users. Easy low hanging fruit to prevent accidents.
CREATE VIEW aaa.user (id, primary_email_id) AS
	SELECT id, primary_email_id
	FROM shadow.aaa_user
	WHERE active = TRUE;

-- Also torn between whether or not I should expose this view or not. Note
-- it's a VIEW created from a JOIN of two VIEWs.
CREATE VIEW aaa.user_emails (user_id, email_id, email, user_primary_email_id) AS
	SELECT u.id, e.id, e.email, u.primary_email_id
	FROM aaa.email AS e, aaa.user AS u
	WHERE e.user_id = u.id;

-- Create a convenience function to SHA256 hash some data. Putting this
-- function in the public schema since it doesn't actually change the state
-- of any tables.
CREATE FUNCTION public.sha256(BYTEA) RETURNS TEXT AS $$
    SELECT encode(public.digest($1, 'sha256'), 'hex')
$$ LANGUAGE SQL STRICT IMMUTABLE;
CREATE FUNCTION public.sha256(TEXT) RETURNS TEXT AS $$
    SELECT encode(public.digest($1, 'sha256'), 'hex')
$$ LANGUAGE SQL STRICT IMMUTABLE;

-- Create a function to register a new user SECURITY DEFINER set to log a
-- user in. Example: SELECT aaa.register(email := 'user@example.com', password := 'myfailpw', ip_address := '11.22.33.44');
CREATE FUNCTION aaa.register(email TEXT, password TEXT, ip_address INET) RETURNS RECORD AS $$
DECLARE
	ret RECORD;
	a_email      ALIAS FOR email;
	a_password   ALIAS FOR password;
	a_ip_address ALIAS FOR ip_address;
	v_email_id        shadow.aaa_email.id%TYPE;
	v_user_id         shadow.aaa_user.id%TYPE;
	v_hashed_password shadow.aaa_user.hashpass%TYPE;
BEGIN
	-- Check that the email isn't already in use
	SELECT e.id INTO v_email_id FROM shadow.aaa_email AS e WHERE e.email = a_email LIMIT 1;
	IF found THEN
		-- Should log that this IP address attempted a failed registration
		ret := (FALSE, 'email'::TEXT, 'email address already in use'::TEXT);
		RETURN ret;
	END IF;

	-- Hash the user's password.
	v_hashed_password := public.sha256(a_password);

	-- Create a new user and email. Create the aaa_email record because
	-- it is smaller and we need to perform an UPDATE to resolve the
	-- circular FOREIGN KEYS.
	INSERT INTO shadow.aaa_email (email, user_id) VALUES (a_email, 0) RETURNING id INTO STRICT v_email_id;
	INSERT INTO shadow.aaa_user (hashpass, primary_email_id, registration_utc, registration_ip) VALUES (v_hashed_password, v_email_id, NOW(), a_ip_address) RETURNING id INTO STRICT v_user_id;
	UPDATE shadow.aaa_email SET user_id = v_user_id WHERE id = v_email_id;
	ret := (TRUE, NULL::TEXT, NULL::TEXT);
	RETURN ret;
END;
$$
	LANGUAGE plpgsql
	RETURNS NULL ON NULL INPUT
	SECURITY DEFINER;

-- END: aaa's database objects
