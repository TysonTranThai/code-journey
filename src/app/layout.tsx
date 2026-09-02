import type { Metadata, Viewport } from "next";

import { SiteHeader } from "@/components/layout/SiteHeader";
import { siteConfig } from "@/lib/site-config";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: {
    default: `${siteConfig.name} — ${siteConfig.tagline}`,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col bg-zinc-950 text-zinc-100">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-zinc-900 focus:px-4 focus:py-2 focus:text-white"
        >
          Skip to main content
        </a>
        <SiteHeader />
        <div className="flex flex-1 flex-col">{children}</div>
        <footer className="border-t border-zinc-800">
          <div className="mx-auto max-w-6xl px-6 py-6 text-sm text-zinc-400">
            Free and open education. Built in the open.
          </div>
        </footer>
      </body>
    </html>
  );
}
