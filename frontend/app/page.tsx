"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import dynamic from "next/dynamic";
import { Moon, ScanSearch, Sun, Wifi, WifiOff, Clock3, X, UploadCloud } from "lucide-react";
import type { Edge, Node } from "reactflow";
import AIPanel from "@/components/AIPanel";
import ResultCard from "@/components/ResultCard";
import VTChart from "@/components/VTChart";
import { buildGraph, type SearchResponse } from "@/lib/buildGraph";

const GraphView = dynamic(() => import("@/components/GraphView"), { ssr: false });

type WsStatus = "connecting" | "connected" | "disconnected" | "error";
type Theme = "light" | "dark";
type QueryKind = "ip" | "domain" | "email" | "hash" | "phone" | "username" | "unknown";

interface Toast {
  id: string;
  message: string;
}

interface HistoryEntry {
  query: string;
  type: QueryKind;
}

const WS_STATUS: Record<WsStatus, string> = {
  connecting: "text-amber-500 dark:text-amber-300",
  connected: "text-emerald-600 dark:text-emerald-300",
  disconnected: "text-slate-500 dark:text-slate-400",
  error: "text-red-600 dark:text-red-300",
};

const HISTORY_KEY = "omnitrace:search-history";

function detectQueryType(query: string): QueryKind {
  const q = query.trim();
  if (!q) return "unknown";
  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(q)) return "ip";
  if (/^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$/.test(q)) return "email";
  if (/^\+?[\d()\s-]{8,}$/.test(q)) return "phone";
  if (/^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$/.test(q)) return "hash";
  if (/^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(\.[A-Za-z0-9-]{1,63})+$/.test(q)) return "domain";
  if (/^[a-zA-Z0-9_.-]{3,}$/.test(q)) return "username";
  return "unknown";
}

function formatKind(kind: QueryKind): string {
  if (kind === "unknown") return "auto";
  return kind;
}

function parseVirusTotalCounts(results: SearchResponse["results"]): Record<string, number> | null {
  const vt = results.find((result) => result.source.toLowerCase() === "virustotal" && result.success && result.data);
  if (!vt?.data) return null;
  return {
    malicious: Number(vt.data.malicious || 0),
    suspicious: Number(vt.data.suspicious || 0),
    harmless: Number(vt.data.harmless || 0),
    undetected: Number(vt.data.undetected || 0),
  };
}

export default function OmniTraceDashboard() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [graphNodes, setGraphNodes] = useState<Node[]>([]);
  const [graphEdges, setGraphEdges] = useState<Edge[]>([]);
  const [loading, setLoading] = useState(false);
  const [wsStatus, setWsStatus] = useState<WsStatus>("connecting");
  const [theme, setTheme] = useState<Theme>("dark");
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [sandboxValue, setSandboxValue] = useState("");
  const [sandboxFile, setSandboxFile] = useState<File | null>(null);
  const [isDragActive, setIsDragActive] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);
  const searchInputRef = useRef<HTMLInputElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const queryType = useMemo(() => detectQueryType(query), [query]);

  const pushToast = useCallback((message: string) => {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    setToasts((prev) => [...prev, { id, message }]);
    window.setTimeout(() => {
      setToasts((prev) => prev.filter((item) => item.id !== id));
    }, 4000);
  }, []);

  const applySearchResult = useCallback(
    (payload: SearchResponse) => {
      setResults(payload);
      const graph = buildGraph(payload);
      setGraphNodes(graph.nodes);
      setGraphEdges(graph.edges);
      if (payload.cached) pushToast("Showing cached results.");
      setHistory((prev) => {
        const next = [{ query: payload.query, type: detectQueryType(payload.query) }, ...prev.filter((entry) => entry.query !== payload.query)].slice(0, 10);
        localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
        return next;
      });
    },
    [pushToast],
  );

  useEffect(() => {
    const stored = localStorage.getItem(HISTORY_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored) as HistoryEntry[];
        setHistory(Array.isArray(parsed) ? parsed.slice(0, 10) : []);
      } catch {
        setHistory([]);
      }
    }

    const isDark = document.documentElement.classList.contains("dark");
    setTheme(isDark ? "dark" : "light");
  }, []);

  useEffect(() => {
    const onShortcut = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        searchInputRef.current?.focus();
      }
    };

    window.addEventListener("keydown", onShortcut);
    return () => window.removeEventListener("keydown", onShortcut);
  }, []);

  useEffect(() => {
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let reconnectAttempts = 0;
    const maxAttempts = 5;
    const baseDelay = 1000;

    const connect = () => {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const wsUrl = `${base.replace(/^http(s?)/, (_m, secure: string) => (secure ? "wss" : "ws"))}/ws`;
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;
      setWsStatus("connecting");

      ws.onopen = () => {
        reconnectAttempts = 0;
        setWsStatus("connected");
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as SearchResponse;
          applySearchResult(data);
        } catch {
          pushToast("Received malformed data from WebSocket.");
        } finally {
          setLoading(false);
        }
      };

      ws.onerror = () => {
        setWsStatus("error");
      };

      ws.onclose = () => {
        setWsStatus("disconnected");
        if (reconnectAttempts < maxAttempts) {
          const delay = baseDelay * 2 ** reconnectAttempts;
          pushToast(`WebSocket reconnecting in ${Math.round(delay / 1000)}s (attempt ${reconnectAttempts + 1}/${maxAttempts})`);
          reconnectTimer = setTimeout(connect, delay);
          reconnectAttempts += 1;
          return;
        }
        pushToast("WebSocket unavailable, using REST fallback.");
      };
    };

    connect();

    return () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      wsRef.current?.close();
    };
  }, [applySearchResult, pushToast]);

  const performSearch = useCallback(
    async (rawQuery?: string) => {
      const q = (rawQuery ?? query).trim();
      if (!q) return;
      setLoading(true);

      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ query: q, query_type: "auto" }));
        return;
      }

      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const response = await fetch(`${apiUrl}/search`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: q, query_type: "auto" }),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const payload = (await response.json()) as SearchResponse;
        applySearchResult(payload);
      } catch {
        pushToast("Search failed. Please try again.");
      } finally {
        setLoading(false);
      }
    },
    [applySearchResult, pushToast, query],
  );

  const toggleTheme = () => {
    const nextTheme: Theme = theme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
    const useDark = nextTheme === "dark";
    document.documentElement.classList.toggle("dark", useDark);
    localStorage.setItem("theme", nextTheme);
  };

  const removeHistoryItem = (itemQuery: string) => {
    setHistory((prev) => {
      const next = prev.filter((entry) => entry.query !== itemQuery);
      localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
      return next;
    });
  };

  const onFileSelect = (fileList: FileList | null) => {
    const file = fileList?.[0] ?? null;
    setSandboxFile(file);
  };

  const submitSandbox = () => {
    const hasContent = sandboxValue.trim() || sandboxFile;
    if (!hasContent) return;
    const jobId = `SAN-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
    pushToast(`Submitted! Job ID: ${jobId}`);
    setSandboxValue("");
    setSandboxFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const vtData = results ? parseVirusTotalCounts(results.results) : null;

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-100 transition-colors">
      <div className="fixed top-4 right-4 z-50 space-y-2 w-[320px] max-w-[calc(100vw-2rem)]">
        {toasts.map((toast) => (
          <div key={toast.id} className="toast-enter rounded-lg border border-slate-700 bg-slate-900/95 text-slate-100 px-3 py-2 text-sm shadow-lg">
            {toast.message}
          </div>
        ))}
      </div>

      <div className="mx-auto max-w-7xl px-4 py-8 space-y-8">
        <header className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center">
              <ScanSearch className="w-5 h-5 text-blue-500 dark:text-blue-300" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold">OmniTrace Dashboard</h1>
              <p className="text-sm text-slate-600 dark:text-slate-400">Ethical OSINT Intelligence Platform</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className={`inline-flex items-center gap-2 rounded-full border border-slate-600 px-3 py-1 text-xs font-medium bg-white/80 dark:bg-slate-900/70 ${WS_STATUS[wsStatus]}`}>
              {wsStatus === "connected" ? <Wifi className="w-3.5 h-3.5" /> : <WifiOff className="w-3.5 h-3.5" />}
              <span className="relative inline-flex h-2 w-2">
                <span className={`absolute inline-flex h-full w-full rounded-full ${wsStatus === "connected" ? "bg-emerald-400" : "bg-amber-400"} opacity-75 animate-ping`} />
                <span className={`relative inline-flex rounded-full h-2 w-2 ${wsStatus === "connected" ? "bg-emerald-500" : "bg-amber-500"}`} />
              </span>
              WS {wsStatus}
            </span>
            <button
              type="button"
              onClick={toggleTheme}
              className="rounded-lg border border-slate-600 p-2 bg-white/80 hover:bg-white dark:bg-slate-900/70 dark:hover:bg-slate-800"
              aria-label="Toggle theme"
            >
              {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        </header>

        <section className="rounded-2xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-6 shadow-sm">
          <div className="mx-auto max-w-3xl space-y-4">
            <div className="flex items-center gap-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-4 py-3">
              <input
                ref={searchInputRef}
                type="text"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") performSearch();
                }}
                className="flex-1 bg-transparent outline-none text-base"
                placeholder="Search IP, domain, email, username, hash, phone…"
              />
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-600/15 text-blue-600 dark:text-blue-300 border border-blue-500/30">
                {formatKind(queryType)}
              </span>
            </div>
            <div className="flex justify-center">
              <button
                type="button"
                onClick={() => performSearch()}
                disabled={!query.trim() || loading}
                className="px-8 py-2.5 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-500 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {loading ? "Searching…" : "Search & Analyze"}
              </button>
            </div>
            <p className="text-center text-xs text-slate-500 dark:text-slate-400">Press Ctrl+K / Cmd+K to focus search</p>
          </div>
        </section>

        {loading && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="space-y-3 lg:col-span-1">
              {[0, 1, 2].map((item) => (
                <div key={item} className="h-24 rounded-xl bg-slate-200 dark:bg-slate-800 animate-pulse" />
              ))}
            </div>
            <div className="lg:col-span-2 h-[520px] rounded-xl bg-slate-200 dark:bg-slate-800 animate-pulse" />
          </div>
        )}

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-4">
            <div className="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-4">
              <h2 className="text-lg font-semibold mb-3">Intelligence Results</h2>
              {!results && !loading ? (
                <p className="text-sm text-slate-500 dark:text-slate-400">Run a search to populate results.</p>
              ) : null}

              {results ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                    <span className="px-2 py-0.5 rounded-full bg-slate-200 dark:bg-slate-800">{results.query_type}</span>
                    {results.cached ? <span className="px-2 py-0.5 rounded-full bg-amber-200/60 dark:bg-amber-900/30">cached</span> : null}
                    <span className="ml-auto">{results.results.length} sources</span>
                  </div>

                  {results.ai_summary ? <AIPanel summary={results.ai_summary} streaming={loading} /> : null}
                  {vtData ? <VTChart data={vtData} /> : null}

                  <div className="space-y-3 max-h-[420px] overflow-y-auto scrollbar-thin-dark pr-1">
                    {results.results.map((result) => (
                      <ResultCard key={result.source} result={result} />
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </div>

          <div className="lg:col-span-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-4 h-[620px]">
            <h2 className="text-lg font-semibold mb-3">Relationship Graph</h2>
            <GraphView nodes={graphNodes} edges={graphEdges} />
          </div>
        </section>

        <section className="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-4">
          <div className="flex items-center gap-2 mb-3">
            <Clock3 className="w-4 h-4" />
            <h3 className="text-sm font-semibold">Recent searches</h3>
          </div>
          {history.length === 0 ? (
            <p className="text-sm text-slate-500 dark:text-slate-400">No search history yet.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {history.map((entry) => (
                <div key={entry.query} className="inline-flex items-center gap-1 rounded-full border border-slate-500/40 px-2 py-1 text-xs">
                  <button
                    type="button"
                    onClick={() => {
                      setQuery(entry.query);
                      performSearch(entry.query);
                    }}
                    className="hover:text-blue-500"
                  >
                    {entry.query}
                  </button>
                  <span className="px-1.5 rounded-full bg-blue-600/15 text-blue-500 dark:text-blue-300">{entry.type}</span>
                  <button
                    type="button"
                    onClick={() => removeHistoryItem(entry.query)}
                    className="text-slate-400 hover:text-red-400"
                    aria-label={`Remove ${entry.query}`}
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-4 space-y-3">
          <h2 className="text-lg font-semibold">Sandbox Analysis</h2>
          <textarea
            value={sandboxValue}
            onChange={(event) => setSandboxValue(event.target.value)}
            placeholder="Paste URL or hash for sandbox submission…"
            className="w-full min-h-24 rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          />

          <div
            onDragOver={(event) => {
              event.preventDefault();
              setIsDragActive(true);
            }}
            onDragLeave={() => setIsDragActive(false)}
            onDrop={(event) => {
              event.preventDefault();
              setIsDragActive(false);
              onFileSelect(event.dataTransfer.files);
            }}
            onClick={() => fileInputRef.current?.click()}
            className={`rounded-lg border-2 border-dashed p-4 text-sm cursor-pointer transition ${
              isDragActive ? "border-blue-500 bg-blue-500/10" : "border-slate-400/50 hover:border-blue-500/60"
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={(event) => onFileSelect(event.target.files)}
            />
            <div className="flex items-center gap-2">
              <UploadCloud className="w-4 h-4" />
              <span>{sandboxFile ? `Selected: ${sandboxFile.name}` : "Drag and drop file here or click to choose"}</span>
            </div>
          </div>

          <button
            type="button"
            onClick={submitSandbox}
            disabled={!sandboxValue.trim() && !sandboxFile}
            className="px-4 py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            Submit for Analysis
          </button>
        </section>
      </div>
    </div>
  );
}
