-- env PGDATABASES=skeleton PGUSER=skeleton_dba

CREATE UNIQUE INDEX user_id_udx
  ON aaa.user(id);

CREATE UNIQUE INDEX timezone_name_lower_udx
  ON public.timezone(LOWER(name));

CREATE UNIQUE INDEX email_email_lower_udx
  ON shadow.aaa_email(LOWER(email));

CREATE INDEX aaa_email_confirmation_log_email_idx
  ON shadow.aaa_email_confirmation_log(email_id);
CREATE INDEX aaa_email_confirmation_log_confirmation_code_idx
  ON shadow.aaa_email_confirmation_log(confirmation_code);

CREATE INDEX aaa_login_attempts_user_login_idx
  ON shadow.aaa_login_attempts(user_id, login_utc);

-- Use a UNIQUE INDEX for valid sessions and a non-UNIQUE INDEX for expired
-- sessions.
CREATE UNIQUE INDEX aaa_session_id_valid_true_udx
  ON shadow.aaa_session(session_id) WHERE valid = TRUE;
CREATE INDEX aaa_session_id_valid_false_idx
  ON shadow.aaa_session(session_id) WHERE valid = FALSE;

-- A periodic cronjob should mark session invalid based on 'end_utc < NOW()'
CREATE INDEX aaa_session_end_utc_idx
  ON shadow.aaa_session(end_utc) WHERE valid = TRUE;

-- Use an index scan for a particular user_id to make sure that the number of
-- concurrent session for a user is less than the user's configured max
-- number of concurrent sessions.
CREATE INDEX aaa_session_user_id_idx
  ON shadow.aaa_session(user_id) WHERE valid = TRUE;

CREATE UNIQUE INDEX aaa_user_primary_email_udx
  ON shadow.aaa_user(primary_email_id);
