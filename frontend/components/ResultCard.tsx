"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, CheckCircle, XCircle } from "lucide-react";

interface IntegrationResult {
  source: string;
  success: boolean;
  data: Record<string, unknown> | null;
  error: string | null;
}

export default function ResultCard({ result }: { result: IntegrationResult }) {
  const [expanded, setExpanded] = useState(true);

  const sourceLabel = result.source.toUpperCase();

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-xl overflow-hidden">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-slate-700/40 transition"
      >
        <div className="flex items-center gap-2">
          {result.success ? (
            <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
          ) : (
            <XCircle className="w-4 h-4 text-red-400 shrink-0" />
          )}
          <span className="font-semibold text-sm">{sourceLabel}</span>
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
      </button>

      {expanded && (
        <div className="px-4 pb-4">
          {result.success && result.data ? (
            <DataTable data={result.data} />
          ) : (
            <p className="text-red-400 text-sm">{result.error || "No data"}</p>
          )}
        </div>
      )}
    </div>
  );
}

function DataTable({ data }: { data: Record<string, unknown> }) {
  return (
    <table className="w-full text-xs">
      <tbody>
        {Object.entries(data).map(([key, value]) => {
          if (value === null || value === undefined || value === "" || (Array.isArray(value) && value.length === 0))
            return null;
          return (
            <tr key={key} className="border-b border-slate-700/50 last:border-0">
              <td className="py-1.5 pr-3 text-slate-400 font-medium capitalize w-32 align-top">
                {key.replace(/_/g, " ")}
              </td>
              <td className="py-1.5 text-slate-200 font-mono break-all">
                {Array.isArray(value) ? (
                  <ul className="space-y-0.5">
                    {(value as unknown[]).slice(0, 10).map((v, i) => (
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
