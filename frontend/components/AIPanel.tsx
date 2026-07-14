"use client";

import { useEffect, useMemo, useState } from "react";
import { Check, Copy, Sparkles } from "lucide-react";

interface AIPanelProps {
  summary: string;
  streaming?: boolean;
}

export default function AIPanel({ summary, streaming = false }: AIPanelProps) {
  const [shown, setShown] = useState(streaming ? "" : summary);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!streaming) {
      setShown(summary);
      return;
    }

    setShown("");
    let index = 0;
    const timer = window.setInterval(() => {
      index += 1;
      setShown(summary.slice(0, index));
      if (index >= summary.length) window.clearInterval(timer);
    }, 20);

    return () => window.clearInterval(timer);
  }, [summary, streaming]);

  const content = useMemo(() => (streaming ? shown : summary), [shown, streaming, summary]);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(summary);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1200);
  };

  return (
    <div className="bg-gradient-to-br from-blue-900/30 to-indigo-900/30 border border-blue-700/40 rounded-xl p-4 space-y-2">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 text-blue-300 font-semibold text-sm">
          <Sparkles className="w-4 h-4" />
          AI Intelligence Summary
        </div>
        <button
          type="button"
          onClick={copyToClipboard}
          className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 transition"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <p className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">
        {content}
        {streaming && content.length < summary.length && <span className="typewriter-cursor">|</span>}
      </p>
    </div>
  );
}
