"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search } from "lucide-react";

export default function Home() {
  const [query, setQuery] = useState("");
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const q = query.trim();
    if (!q) return;
    router.push(`/search?q=${encodeURIComponent(q)}`);
  };

  const examples = [
    { label: "IP Address", value: "8.8.8.8" },
    { label: "Domain", value: "example.com" },
    { label: "Email", value: "test@example.com" },
    { label: "Hash (MD5)", value: "d41d8cd98f00b204e9800998ecf8427e" },
  ];

  return (
    <div className="flex flex-col items-center justify-center py-20 gap-10">
      <div className="text-center space-y-3">
        <h1 className="text-5xl font-extrabold tracking-tight">
          <span className="text-brand-500">Omni</span>Trace
        </h1>
        <p className="text-slate-400 text-lg max-w-xl">
          AI-enhanced OSINT: search IPs, domains, emails, hashes, and more.
          Aggregates Shodan, VirusTotal, WHOIS, DNS, HIBP in parallel.
        </p>
      </div>

      <form onSubmit={handleSearch} className="w-full max-w-2xl">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search IP, domain, email, hash, username…"
              className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-600 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-3 bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl transition disabled:opacity-50"
            disabled={!query.trim()}
          >
            Search
          </button>
        </div>
      </form>

      <div className="flex flex-wrap gap-2 justify-center">
        {examples.map((ex) => (
          <button
            key={ex.value}
            onClick={() => setQuery(ex.value)}
            className="px-3 py-1.5 text-sm bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-slate-300 transition"
          >
            <span className="text-slate-500 mr-1">{ex.label}:</span>
            {ex.value}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4 w-full max-w-3xl">
        {[
          { icon: "🌐", title: "IP / Domain", desc: "Shodan, VirusTotal, WHOIS, DNS" },
          { icon: "📧", title: "Email", desc: "HaveIBeenPwned breach check" },
          { icon: "🔐", title: "File Hash", desc: "VirusTotal malware scan" },
          { icon: "🤖", title: "AI Summary", desc: "LiteLLM-powered intelligence" },
        ].map((f) => (
          <div key={f.title} className="bg-slate-800/50 border border-slate-700 rounded-xl p-4 space-y-1">
            <div className="text-2xl">{f.icon}</div>
            <div className="font-semibold text-sm">{f.title}</div>
            <div className="text-xs text-slate-400">{f.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
