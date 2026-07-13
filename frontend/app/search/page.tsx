import { Suspense } from "react";
import SearchPageClient from "./SearchPageClient";

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="py-8 text-center text-slate-400">Loading search…</div>}>
      <SearchPageClient />
    </Suspense>
  );
}
