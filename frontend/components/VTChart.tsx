"use client";

import { useMemo, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Bar,
  CartesianGrid,
} from "recharts";

const COLORS: Record<string, string> = {
  malicious: "#ef4444",
  suspicious: "#f97316",
  harmless: "#22c55e",
  undetected: "#64748b",
};

interface Props {
  data: Record<string, number>;
}

function riskLabel(malicious: number, suspicious: number) {
  if (malicious > 0) return { text: "HIGH RISK", cls: "bg-red-900/40 text-red-300 border-red-700" };
  if (suspicious > 0) return { text: "SUSPICIOUS", cls: "bg-amber-900/40 text-amber-300 border-amber-700" };
  return { text: "CLEAN", cls: "bg-emerald-900/40 text-emerald-300 border-emerald-700" };
}

export default function VTChart({ data }: Props) {
  const [mode, setMode] = useState<"pie" | "bar">("pie");

  const chartData = useMemo(
    () =>
      Object.entries(data)
        .filter(([k, v]) => k in COLORS && typeof v === "number" && v > 0)
        .map(([name, value]) => ({ name, value })),
    [data],
  );

  if (chartData.length === 0) return null;

  const malicious = Number(data.malicious || 0);
  const suspicious = Number(data.suspicious || 0);
  const harmless = Number(data.harmless || 0);
  const undetected = Number(data.undetected || 0);
  const total = malicious + suspicious + harmless + undetected;
  const risk = riskLabel(malicious, suspicious);

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h3 className="font-semibold text-sm text-slate-300">VirusTotal Detection Breakdown</h3>
        <div className="inline-flex rounded-lg border border-slate-600 overflow-hidden text-xs">
          <button
            type="button"
            onClick={() => setMode("pie")}
            className={`px-3 py-1.5 ${mode === "pie" ? "bg-blue-600 text-white" : "bg-slate-900 text-slate-300"}`}
          >
            Pie
          </button>
          <button
            type="button"
            onClick={() => setMode("bar")}
            className={`px-3 py-1.5 ${mode === "bar" ? "bg-blue-600 text-white" : "bg-slate-900 text-slate-300"}`}
          >
            Bar
          </button>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2 text-xs text-slate-300">
        <span>{malicious} malicious • {suspicious} suspicious • {harmless} harmless • {undetected} undetected</span>
        <span className={`px-2 py-0.5 rounded border font-semibold ${risk.cls}`}>{risk.text}</span>
      </div>

      <p className="text-xs text-slate-400">Detection summary: {malicious + suspicious} flagged out of {total || 0} engines.</p>

      <ResponsiveContainer width="100%" height={220}>
        {mode === "pie" ? (
          <PieChart>
            <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
              {chartData.map((entry) => (
                <Cell key={entry.name} fill={COLORS[entry.name] || "#94a3b8"} />
              ))}
            </Pie>
            <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "8px", color: "#f1f5f9" }} />
            <Legend />
          </PieChart>
        ) : (
          <BarChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
            <YAxis stroke="#94a3b8" allowDecimals={false} fontSize={12} />
            <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "8px", color: "#f1f5f9" }} />
            <Bar dataKey="value">
              {chartData.map((entry) => (
                <Cell key={entry.name} fill={COLORS[entry.name] || "#94a3b8"} />
              ))}
            </Bar>
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
