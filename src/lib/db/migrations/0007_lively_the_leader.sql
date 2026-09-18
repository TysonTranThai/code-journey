ALTER TABLE "users" ADD COLUMN "last_active_at" timestamp with time zone;

-- Backfill: seed existing users from the best VERIFIED activity evidence that
-- already exists, instead of inventing history. "Verified evidence" = the
-- user actually did something server-verified:
--   MAX(submissions.created_at)     (ran a challenge)
--   MAX(progress_events.created_at) (completed content)
--   MAX(comments.created_at)        (posted in a discussion)
--   MAX(mentor_requests.created_at) (used the mentor)
-- The greatest of these is a conservative lower bound on true activity.
--
-- Safety properties of this backfill:
--   1. Accounts WITH evidence  -> lastActiveAt = latest evidence (not older).
--   2. Accounts with NO evidence -> stays NULL. The cleanup NEVER deletes
--      NULL-activity accounts, so pre-existing dormant accounts are safe.
--   3. No invented timestamps anywhere.
-- Idempotent on re-run: rows with non-NULL values would only be overwritten
-- with NULL (impossible — evidence IS NOT NULL guards each row), so re-runs
-- are harmless; drizzle applies each migration once anyway.

WITH evidence AS (
  SELECT u.id,
         GREATEST(
           (SELECT MAX(s.created_at) FROM submissions s WHERE s.user_id = u.id),
           (SELECT MAX(p.created_at) FROM progress_events p WHERE p.user_id = u.id),
           (SELECT MAX(c.created_at) FROM comments c WHERE c.user_id = u.id),
           (SELECT MAX(m.created_at) FROM mentor_requests m WHERE m.user_id = u.id)
         ) AS last_evidence
  FROM users u
)
UPDATE users
SET last_active_at = evidence.last_evidence
FROM evidence
WHERE users.id = evidence.id
  AND evidence.last_evidence IS NOT NULL;
