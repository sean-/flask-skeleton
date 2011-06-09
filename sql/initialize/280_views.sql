-- env PGDATABASE=skeleton PGUSER=skeleton_dba

-- A view to SELECT user data. Explicitly don't include the primary_email_id
-- or registration_ip. Users must always present their own email address and
-- have their email address used to lookup their email_id.
CREATE OR REPLACE VIEW
aaa.user (id, active, registration_utc, max_concurrent_sessions,
         default_ipv4_mask, default_ipv6_mask, timezone_id) AS
  SELECT
    u.id, u.active, u.registration_utc, u.max_concurrent_sessions,
    u.default_ipv4_mask, u.default_ipv6_mask, ui.timezone_id
  FROM
    shadow.aaa_user AS u, aaa.user_info AS ui
  WHERE u.id = ui.id;


-- Enable this view in the email schema since access to email data should
-- only be done via functions. Under no circumstances should a web process be
-- able to do a 'SELECT *' on email or user information. email batch jobs
-- have access to this data via the email schema (the web user does not have
-- access to this schema, just like the email role does not have access to
-- the rest of the schemas).
CREATE OR REPLACE VIEW
email.email (id, email, user_id) AS
  SELECT
    e.id, e.email, e.user_id
  FROM
    shadow.aaa_email AS e, shadow.aaa_email_confirmation_log AS ecl
  WHERE
    e.id = ecl.email_id AND ecl.confirmed = TRUE;


-- Only show active users. Easy low hanging fruit to prevent accidents.
CREATE OR REPLACE VIEW
email."user" (id, primary_email_id) AS
  SELECT id, primary_email_id
  FROM shadow.aaa_user
  WHERE active = TRUE;


-- Note this view is created from a JOIN of two VIEWs. Again, in the email
-- schema because no one web process should have access to see every email
-- address in the system.
CREATE OR REPLACE VIEW
email.user_emails (user_id, email_id, email, user_primary_email_id) AS
  SELECT u.id, e.id, e.email, u.primary_email_id
  FROM email.email AS e, email."user" AS u
  WHERE e.user_id = u.id;
