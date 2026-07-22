const configuredApiUrl = process.env.NEXT_PUBLIC_API_URL?.trim();

export function getApiUrl(): string | null {
  if (configuredApiUrl) {
    return configuredApiUrl.replace(/\/+$/, "");
  }

  if (typeof window !== "undefined" && window.location.hostname === "localhost") {
    return "http://localhost:8000";
  }

  return null;
}

export function getWebSocketUrl(apiUrl: string): string {
  return `${apiUrl.replace(/^http(s?)/, (_match, secure: string) => (secure === "s" ? "wss" : "ws"))}/ws`;
}
