"use client";

import { useMemo, useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  CheckCircle,
  XCircle,
  Shield,
  Globe,
  FileText,
  AlertTriangle,
  Database,
  Network,
  Copy,
  Check,
} from "lucide-react";

interface IntegrationResult {
  source: string;
  success: boolean;
  data: Record<string, unknown> | null;
  error: string | null;
}

const sourceMeta: Record<string, { icon: typeof Database; className: string; label: string }> = {
  shodan: { icon: Network, className: "text-blue-300 bg-blue-900/30 border-blue-700/50", label: "Shodan Network" },
  virustotal: { icon: Shield, className: "text-red-300 bg-red-900/30 border-red-700/50", label: "VirusTotal Shield" },
  dns: { icon: Globe, className: "text-purple-300 bg-purple-900/30 border-purple-700/50", label: "DNS Globe" },
  whois: { icon: FileText, className: "text-yellow-300 bg-yellow-900/20 border-yellow-700/50", label: "WHOIS FileText" },
  hibp: { icon: AlertTriangle, className: "text-orange-300 bg-orange-900/30 border-orange-700/50", label: "HIBP AlertTriangle" },
};

function nonNullFieldCount(data: Record<string, unknown> | null): number {
  if (!data) return 0;
  return Object.values(data).filter((value) => {
    if (value === null || value === undefined || value === "") return false;
    if (Array.isArray(value) && value.length === 0) return false;
    return true;
  }).length;
}

export default function ResultCard({ result }: { result: IntegrationResult }) {
  const [expanded, setExpanded] = useState(true);
  const [copied, setCopied] = useState(false);
  const key = result.source.toLowerCase();
  const meta = sourceMeta[key] ?? { icon: Database, className: "text-slate-300 bg-slate-700/40 border-slate-600", label: "Database" };
  const Icon = meta.icon;
  const fieldCount = useMemo(() => nonNullFieldCount(result.data), [result.data]);

  const copyJson = async () => {
    await navigator.clipboard.writeText(JSON.stringify(result.data, null, 2));
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1200);
  };

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-xl overflow-hidden">
      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-slate-700/40 transition"
      >
        <div className="flex items-center gap-2 min-w-0">
          {result.success ? (
            <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
          ) : (
            <XCircle className="w-4 h-4 text-red-400 shrink-0" />
          )}
          <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md border text-xs ${meta.className}`}>
            <Icon className="w-3.5 h-3.5" />
            {meta.label}
          </span>
          <span className="text-slate-400 text-xs">{fieldCount} fields</span>
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
      </button>

      <div className={`grid transition-all duration-300 ${expanded ? "grid-rows-[1fr]" : "grid-rows-[0fr]"}`}>
        <div className="overflow-hidden">
          <div className="px-4 pb-4 space-y-2">
            {result.success && result.data ? (
              <>
                <div className="flex justify-end">
                  <button
                    type="button"
                    onClick={copyJson}
                    className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-md bg-slate-700 hover:bg-slate-600 text-slate-200 transition"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    {copied ? "Copied" : "Copy JSON"}
                  </button>
                </div>
                <DataTable data={result.data} />
              </>
            ) : (
              <p className="text-red-400 text-sm">{result.error || "No data"}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function DataTable({ data }: { data: Record<string, unknown> }) {
  return (
    <table className="w-full text-xs">
      <tbody>
        {Object.entries(data).map(([key, value]) => {
          if (value === null || value === undefined || value === "" || (Array.isArray(value) && value.length === 0)) return null;
          return (
            <tr key={key} className="border-b border-slate-700/50 last:border-0">
              <td className="py-1.5 pr-3 text-slate-400 font-medium capitalize w-32 align-top">{key.replace(/_/g, " ")}</td>
              <td className="py-1.5 text-slate-200 font-mono break-all">
                {Array.isArray(value) ? (
                  <ul className="space-y-0.5">
                    {value.slice(0, 10).map((v, i) => (
                      <li key={i}>{String(v)}</li>
                    ))}
                    {value.length > 10 && <li className="text-slate-500">…+{value.length - 10} more</li>}
                  </ul>
                ) : typeof value === "object" ? (
                  <pre className="whitespace-pre-wrap">{JSON.stringify(value, null, 2)}</pre>
                ) : (
                  String(value)
                )}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
