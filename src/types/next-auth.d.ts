import type { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      role: "student" | "admin";
    } & DefaultSession["user"];
  }

  interface User {
    role?: "student" | "admin";
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    role?: "student" | "admin";
  }
}
