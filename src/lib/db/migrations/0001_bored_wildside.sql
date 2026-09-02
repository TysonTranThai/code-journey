CREATE TYPE "public"."execution_status" AS ENUM('queued', 'claimed', 'running', 'completed', 'failed');--> statement-breakpoint
CREATE TABLE "execution_jobs" (
	"id" text PRIMARY KEY NOT NULL,
	"submission_id" text,
	"status" "execution_status" DEFAULT 'queued' NOT NULL,
	"payload" jsonb NOT NULL,
	"verdict_payload" jsonb,
	"claimed_by" text,
	"claimed_at" timestamp with time zone,
	"started_at" timestamp with time zone,
	"finished_at" timestamp with time zone,
	"attempts" integer DEFAULT 0 NOT NULL,
	"error" text,
	"has_verdict" boolean DEFAULT false NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "submissions" (
	"id" text PRIMARY KEY NOT NULL,
	"user_id" text,
	"challenge_id" text NOT NULL,
	"code" text NOT NULL,
	"verdict" text,
	"per_test_results" jsonb,
	"runtime_ms" integer,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "execution_jobs" ADD CONSTRAINT "execution_jobs_submission_id_submissions_id_fk" FOREIGN KEY ("submission_id") REFERENCES "public"."submissions"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "submissions" ADD CONSTRAINT "submissions_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "execution_jobs_status_idx" ON "execution_jobs" USING btree ("status","created_at");--> statement-breakpoint
CREATE INDEX "submissions_user_challenge_idx" ON "submissions" USING btree ("user_id","challenge_id");