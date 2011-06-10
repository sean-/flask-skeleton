-- env PGDATABASE=skeleton PGUSER=skeleton_root

ALTER TABLE aaa.user ADD CONSTRAINT id_fk
  FOREIGN KEY(id) REFERENCES shadow.aaa_user(id);
ALTER TABLE aaa.user ADD CONSTRAINT timezone_id_fk
  FOREIGN KEY(timezone_id) REFERENCES public.timezone(id);

ALTER TABLE shadow.aaa_email ADD CONSTRAINT email_user_fk
  FOREIGN KEY(user_id) REFERENCES shadow.aaa_user(id) INITIALLY DEFERRED;

ALTER TABLE shadow.aaa_email_confirmation_log ADD CONSTRAINT email_id_fk
  FOREIGN KEY(email_id) REFERENCES shadow.aaa_email(id);

ALTER TABLE shadow.aaa_login_attempts ADD CONSTRAINT user_id_fk
  FOREIGN KEY(user_id) REFERENCES shadow.aaa_user(id);

ALTER TABLE shadow.aaa_session ADD CONSTRAINT user_id_fk
  FOREIGN KEY(user_id) REFERENCES shadow.aaa_user(id);

ALTER TABLE shadow.aaa_user ADD CONSTRAINT primary_email_id_fk
  FOREIGN KEY(primary_email_id) REFERENCES shadow.aaa_email(id);

