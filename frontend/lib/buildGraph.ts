import type { Edge, Node } from "reactflow";

export interface IntegrationResult {
  source: string;
  success: boolean;
  data: Record<string, unknown> | null;
  error: string | null;
}

export interface SearchResponse {
  query: string;
  query_type: string;
  cached: boolean;
  results: IntegrationResult[];
  ai_summary: string | null;
}

const SOURCE_STYLE: Record<string, { emoji: string; color: string; border: string }> = {
  shodan: { emoji: "🌐", color: "#1e40af", border: "#60a5fa" },
  virustotal: { emoji: "🛡️", color: "#7f1d1d", border: "#f87171" },
  dns: { emoji: "🧭", color: "#581c87", border: "#c084fc" },
  whois: { emoji: "📄", color: "#78350f", border: "#facc15" },
  hibp: { emoji: "⚠️", color: "#9a3412", border: "#fdba74" },
};
const RADIAL_DISTANCE = 240;

function sourceUi(source: string) {
  const key = source.toLowerCase();
  return SOURCE_STYLE[key] ?? { emoji: "🗂️", color: "#1f2937", border: "#9ca3af" };
}

export function buildGraph(data: SearchResponse): { nodes: Node[]; edges: Edge[] } {
  const nodes: Node[] = [
    {
      id: "root",
      data: { label: `🔎 ${data.query}\n[${data.query_type}]`, details: data.query },
      position: { x: 0, y: 0 },
      style: {
        background: "#1d4ed8",
        color: "#fff",
        border: "2px solid #3b82f6",
        borderRadius: "12px",
        padding: "10px 16px",
        fontWeight: 700,
      },
    },
  ];
  const edges: Edge[] = [];

  const successful = data.results.filter((r) => r.success);
  const total = Math.max(successful.length, 1);

  successful.forEach((result, i) => {
    const angle = ((2 * Math.PI) / total) * i - Math.PI / 2;
    const sx = Math.round(Math.cos(angle) * RADIAL_DISTANCE);
    const sy = Math.round(Math.sin(angle) * RADIAL_DISTANCE);
    const sourceId = `src-${result.source}`;
    const ui = sourceUi(result.source);

    nodes.push({
      id: sourceId,
      data: {
        label: `${ui.emoji} ${result.source.toUpperCase()}`,
        details: result.data ? `${Object.keys(result.data).length} fields` : "No data",
      },
      position: { x: sx, y: sy },
      style: {
        background: ui.color,
        color: "#f8fafc",
        border: `1px solid ${ui.border}`,
        borderRadius: "10px",
        padding: "8px 12px",
        fontSize: "12px",
        fontWeight: 600,
      },
    });

    edges.push({
      id: `e-root-${result.source}`,
      source: "root",
      target: sourceId,
      animated: true,
      style: { stroke: "#3b82f6", strokeWidth: 2 },
    });

    if (!result.data) return;

    Object.entries(result.data)
      .filter(([, v]) => v !== null && v !== undefined && v !== "")
      .slice(0, 3)
      .forEach(([key, value], j) => {
        const nodeId = `data-${result.source}-${key}`;
        const raw = Array.isArray(value) ? `[${value.length} items]` : String(value);
        const label = `${key}: ${raw.slice(0, 24)}${raw.length > 24 ? "…" : ""}`;

        nodes.push({
          id: nodeId,
          data: { label, details: raw },
          position: { x: sx + (j - 1) * 160, y: sy + 130 },
          style: {
            background: "#0f172a",
            color: "#cbd5e1",
            border: "1px solid #334155",
            borderRadius: "8px",
            padding: "6px 10px",
            fontSize: "11px",
            maxWidth: "160px",
          },
        });

        edges.push({
          id: `e-${result.source}-${key}`,
          source: sourceId,
          target: nodeId,
          style: { stroke: "#475569" },
        });
      });
  });

  return { nodes, edges };
}
