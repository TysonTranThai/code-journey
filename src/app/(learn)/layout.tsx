export default function LearnLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    // Wide screens: let tool-style pages (challenge workspace) use the room.
    // Article-style pages keep their own max-w caps, so only the shell grows.
    <main
      id="main-content"
      className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6 2xl:max-w-[1800px]"
    >
      {children}
    </main>
  );
}
