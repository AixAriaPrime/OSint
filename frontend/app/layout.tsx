import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OmniTrace – Ethical OSINT",
  description: "OmniTrace – Ethical OSINT Intelligence Platform",
};

const themeScript = `(() => {
  try {
    const stored = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const useDark = stored ? stored === 'dark' : prefersDark;
    document.documentElement.classList.toggle('dark', useDark);
  } catch {}
})();`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-100 antialiased transition-colors">
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
        {children}
      </body>
    </html>
  );
}
