import type { Metadata, Viewport } from "next";

import { SessionProvider } from "@/components/providers/SessionProvider";
import { SiteHeader } from "@/components/layout/SiteHeader";
import { getServerLocale } from "@/lib/i18n/server";
import { HTML_LANG } from "@/lib/i18n/config";
import { getDictionary } from "@/lib/i18n/dictionaries";
import { I18nProvider } from "@/lib/i18n/provider";
import { siteConfig } from "@/lib/site-config";
import { Logo } from "@/components/brand/Logo";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: {
    default: `${siteConfig.name} — ${siteConfig.tagline}`,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  icons: {
    icon: [
      { url: "/icon.svg?v=3", type: "image/svg+xml" },
      { url: "/favicon-32x32.png?v=3", sizes: "32x32", type: "image/png" },
      { url: "/favicon.ico?v=3", sizes: "any" },
    ],
    shortcut: "/favicon.ico?v=3",
    apple: "/apple-touch-icon.png?v=3",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // The cj_locale cookie decides the UI language for the request; the
  // provider seeds client components with the same value so hydration matches.
  const locale = await getServerLocale();
  const d = getDictionary(locale);

  return (
    <html lang={HTML_LANG[locale]}>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html:
              'if("scrollRestoration" in history){history.scrollRestoration="manual"}window.scrollTo(0,0);',
          }}
        />
      </head>
      <body className="flex min-h-screen flex-col bg-[#07090e] text-zinc-100 selection:bg-emerald-500/30 selection:text-emerald-200">
        <SessionProvider>
          <I18nProvider locale={locale}>
            <a
              href="#main-content"
              className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-[#22c55e] focus:px-5 focus:py-2.5 focus:font-bold focus:text-black focus:shadow-[0_0_25px_rgba(34,197,94,0.6)] focus:ring-2 focus:ring-white"
            >
              {d.nav.skipToContent}
            </a>
            <SiteHeader />
            <div className="flex flex-1 flex-col">{children}</div>
            <footer className="border-t border-white/[0.08] bg-[#080b14]/85 backdrop-blur-xl">
              <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-8 text-sm text-zinc-400 sm:flex-row 2xl:max-w-[1800px]">
                <div className="flex items-center gap-2.5">
                  <Logo size="sm" beacon={false} />
                  <span className="font-semibold tracking-tight text-zinc-200">
                    Code Journey
                  </span>
                  <span className="text-zinc-600">/</span>
                  <span className="text-zinc-400">{d.footer.tagline}</span>
                </div>
                <div className="flex items-center gap-4 text-xs text-zinc-400 font-mono">
                  <span>{d.footer.features}</span>
                </div>
              </div>
            </footer>
          </I18nProvider>
        </SessionProvider>
      </body>
    </html>
  );
}
