"use client";

import { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import type { Node, Edge } from "reactflow";
import ResultCard from "@/components/ResultCard";
import AIPanel from "@/components/AIPanel";

const GraphView = dynamic(() => import("@/components/GraphView"), { ssr: false });

interface IntegrationResult {
  source: string;
  success: boolean;
  data: Record<string, unknown> | null;
  error: string | null;
}

interface SearchResponse {
  query: string;
  query_type: string;
  cached: boolean;
  results: IntegrationResult[];
  ai_summary: string | null;
}

type WsStatus = "connecting" | "connected" | "disconnected" | "error";
type LoadingState = "idle" | "loading" | "done" | "error";

const WS_STATUS_CLASS: Record<WsStatus, string> = {
  connecting: "text-yellow-400",
  connected: "text-green-400",
  disconnected: "text-slate-400",
  error: "text-red-400",
};

function buildGraph(data: SearchResponse): { nodes: Node[]; edges: Edge[] } {
  const nodes: Node[] = [];
  const edges: Edge[] = [];

  nodes.push({
    id: "root",
    data: { label: `${data.query}\n[${data.query_type}]` },
    position: { x: 0, y: 0 },
    style: {
      background: "#1d4ed8",
      color: "#fff",
      border: "2px solid #3b82f6",
      borderRadius: "8px",
      padding: "10px 16px",
      fontWeight: 600,
    },
  });

  const successful = data.results.filter((r) => r.success);
  const total = successful.length;

  successful.forEach((result, i) => {
    const angle = ((2 * Math.PI) / Math.max(total, 1)) * i - Math.PI / 2;
    const sx = Math.cos(angle) * 220;
    const sy = Math.sin(angle) * 220;

    nodes.push({
      id: `src-${result.source}`,
      data: { label: result.source.toUpperCase() },
      position: { x: sx, y: sy },
      style: {
        background: "#065f46",
        color: "#ecfdf5",
        border: "1px solid #10b981",
        borderRadius: "8px",
        padding: "8px 12px",
        fontSize: "12px",
        fontWeight: 600,
      },
    });

    edges.push({
      id: `e-root-${result.source}`,
      source: "root",
      target: `src-${result.source}`,
      animated: true,
      style: { stroke: "#3b82f6", strokeWidth: 2 },
    });

    if (result.data) {
      Object.entries(result.data)
        .filter(([, v]) => v !== null && v !== undefined && v !== "")
        .slice(0, 3)
        .forEach(([key, value], j) => {
          const nodeId = `data-${result.source}-${key}`;
          const raw = Array.isArray(value)
            ? `[${(value as unknown[]).length} items]`
            : String(value);
          const label = `${key}: ${raw.slice(0, 28)}${raw.length > 28 ? "…" : ""}`;

          nodes.push({
            id: nodeId,
            data: { label },
            position: { x: sx + (j - 1) * 160, y: sy + 130 },
            style: {
              background: "#1e293b",
              color: "#94a3b8",
              border: "1px solid #334155",
              borderRadius: "6px",
              padding: "6px 10px",
              fontSize: "11px",
            },
          });

          edges.push({
            id: `e-${result.source}-${key}`,
            source: `src-${result.source}`,
            target: nodeId,
            style: { stroke: "#334155" },
          });
        });
    }
  });

  return { nodes, edges };
}

export default function OmniTraceDashboard() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [graphNodes, setGraphNodes] = useState<Node[]>([]);
  const [graphEdges, setGraphEdges] = useState<Edge[]>([]);
  const [wsStatus, setWsStatus] = useState<WsStatus>("connecting");
  const [loadingState, setLoadingState] = useState<LoadingState>("idle");

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let reconnectAttempts = 0;
    const maxAttempts = 5;
    const baseDelay = 1000;

    const connect = () => {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const wsUrl = base.replace(/^http(s?)/, (_match, secure: string) => (secure ? "wss" : "ws")) + "/ws";
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setWsStatus("connected");
        reconnectAttempts = 0;
      };
      ws.onmessage = (event) => {
        const data: SearchResponse = JSON.parse(event.data);
        setResults(data);
        const { nodes, edges } = buildGraph(data);
        setGraphNodes(nodes);
        setGraphEdges(edges);
        setLoadingState("done");
      };
      ws.onerror = () => { setWsStatus("error"); setLoadingState("error"); };
      ws.onclose = () => {
        setWsStatus("disconnected");
        if (reconnectAttempts < maxAttempts) {
          const delay = baseDelay * Math.pow(2, reconnectAttempts);
          console.log(`Reconnecting in ${delay}ms… (attempt ${reconnectAttempts + 1}/${maxAttempts})`);
          reconnectTimer = setTimeout(connect, delay);
          reconnectAttempts++;
        }
      };
    };

    connect();

    return () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      wsRef.current?.close();
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps -- runs once to establish persistent WebSocket connection

  const handleSearch = async () => {
    const q = query.trim();
    if (!q) return;

    setLoadingState("loading");
    setResults(null);

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ query: q, query_type: "auto" }));
    } else {
      // REST fallback when WebSocket is unavailable
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/search`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: q, query_type: "auto" }),
        });
        const data: SearchResponse = await res.json();
        setResults(data);
        const { nodes, edges } = buildGraph(data);
        setGraphNodes(nodes);
        setGraphEdges(edges);
        setLoadingState("done");
      } catch (e) {
        console.error("Search failed:", e);
        setLoadingState("error");
      }
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-4xl font-bold">OmniTrace Intelligence Platform</h1>
        <span className={`text-sm font-medium ${WS_STATUS_CLASS[wsStatus]}`}>
          ● WS {wsStatus}
        </span>
      </div>

      <div className="flex gap-4 mb-8">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
          placeholder="Search IP, domain, email, hash…"
        />
        <button
          onClick={handleSearch}
          disabled={!query.trim() || loadingState === "loading"}
          className="bg-brand-600 hover:bg-brand-700 disabled:opacity-50 px-8 py-3 rounded-lg font-medium transition"
        >
          {loadingState === "loading" ? "Analyzing..." : "Search & Analyze"}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Results Panel */}
        <div className="lg:col-span-1 bg-slate-900 rounded-xl p-6 space-y-4">
          <h2 className="text-xl font-semibold">Intelligence Results</h2>

          {loadingState === "loading" && (
            <p className="text-slate-400 text-sm animate-pulse">Querying intelligence sources...</p>
          )}

          {loadingState === "error" && (
            <p className="text-red-400 text-sm">Search failed. Check the API connection and try again.</p>
          )}

          {results && (
            <>
              <div className="flex flex-wrap gap-2 text-sm text-slate-400">
                <span className="bg-brand-900/40 text-brand-300 px-2 py-0.5 rounded font-mono">
                  {results.query_type}
                </span>
                {results.cached && (
                  <span className="bg-slate-700 px-2 py-0.5 rounded">cached</span>
                )}
                <span className="ml-auto">{results.results.length} sources</span>
              </div>

              {results.ai_summary && <AIPanel summary={results.ai_summary} />}

              <div className="space-y-3">
                {results.results.map((r) => (
                  <ResultCard key={r.source} result={r} />
                ))}
              </div>
            </>
          )}

          {loadingState === "idle" && (
            <p className="text-slate-500 text-sm">Run a search to see results here.</p>
          )}
        </div>

        {/* Graph Visualization */}
        <div className="lg:col-span-2 bg-slate-900 rounded-xl p-6 h-[600px]">
          <h2 className="text-xl font-semibold mb-4">Relationship Graph</h2>
          <div className="h-[520px] rounded-lg overflow-hidden">
            <GraphView nodes={graphNodes} edges={graphEdges} />
          </div>
        </div>
      </div>

      {/* Sandbox Analysis */}
      <div className="mt-8 bg-slate-900 rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-2">Submit for Sandbox Analysis</h2>
        <p className="text-slate-500 text-sm">
          Upload a file or paste a URL/hash to submit for dynamic sandbox analysis
          via Hybrid Analysis or ANY.RUN.
        </p>
      </div>
    </div>
  );
}
