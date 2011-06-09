CREATE TRIGGER aaa_session_expire_excess_trg BEFORE INSERT ON shadow.aaa_session
  FOR EACH ROW EXECUTE PROCEDURE shadow.aaa_session_expire_excess_trg();

CREATE TRIGGER aaa_session_fixup_end_utc_trg BEFORE UPDATE ON shadow.aaa_session
  FOR EACH ROW EXECUTE PROCEDURE shadow.aaa_session_fixup_end_utc_trg();
