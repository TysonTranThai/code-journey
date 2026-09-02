CREATE TYPE "public"."progress_content_type" AS ENUM('lesson', 'challenge');--> statement-breakpoint
CREATE TABLE "achievements" (
	"id" text PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"achievement_id" text NOT NULL,
	"awarded_at" timestamp (3) with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "achievements_user_achievement_unique" PRIMARY KEY("user_id","achievement_id")
);
--> statement-breakpoint
CREATE TABLE "progress_events" (
	"id" text PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"content_type" "progress_content_type" NOT NULL,
	"content_id" text NOT NULL,
	"created_at" timestamp (3) with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "progress_events_user_content_unique" PRIMARY KEY("user_id","content_type","content_id")
);
--> statement-breakpoint
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "progress_events" ADD CONSTRAINT "progress_events_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "progress_events_user_created_idx" ON "progress_events" USING btree ("user_id","created_at");