import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OmniTrace – Ethical OSINT",
  description: "AI-enhanced Open Source Intelligence platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-900 text-slate-100 antialiased">
        <header className="border-b border-slate-700 bg-slate-800/60 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-6xl mx-auto px-4 h-14 flex items-center gap-3">
            <span className="text-brand-500 font-bold text-xl tracking-tight">⬡ OmniTrace</span>
            <span className="text-slate-500 text-sm">Ethical OSINT</span>
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-4 py-8">{children}</main>
        <footer className="border-t border-slate-800 mt-16 py-6 text-center text-slate-500 text-xs">
          OmniTrace — public data only. Use responsibly and ethically.
        </footer>
      </body>
    </html>
  );
}
