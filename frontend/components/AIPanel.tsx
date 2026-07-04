"use client";

import { Sparkles } from "lucide-react";

export default function AIPanel({ summary }: { summary: string }) {
  return (
    <div className="bg-gradient-to-br from-brand-900/30 to-slate-800/60 border border-brand-700/50 rounded-xl p-4 space-y-2">
      <div className="flex items-center gap-2 text-brand-400 font-semibold text-sm">
        <Sparkles className="w-4 h-4" />
        AI Intelligence Summary
      </div>
      <p className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">{summary}</p>
    </div>
  );
}
