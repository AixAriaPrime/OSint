import { Suspense } from "react";
import SearchPageClient from "./SearchPageClient";

export default function SearchPage() {
<<<<<<< HEAD
=======
  const searchParams = useSearchParams();
  const router = useRouter();
  const q = searchParams.get("q") || "";

  const [query, setQuery] = useState(q);
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const doSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery.trim() }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      setData(await res.json());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (q) doSearch(q);
  }, [q]); // doSearch is defined inline; re-creating it on every render is safe here

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    router.push(`/search?q=${encodeURIComponent(query.trim())}`);
  };

  const vtResult = data?.results.find((r) => r.source === "virustotal");

>>>>>>> origin/main
  return (
    <Suspense fallback={<div className="py-8 text-center text-slate-400">Loading search…</div>}>
      <SearchPageClient />
    </Suspense>
  );
}
