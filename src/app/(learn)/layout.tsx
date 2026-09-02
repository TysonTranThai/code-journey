export default function LearnLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <main id="main-content" className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      {children}
    </main>
  );
}
