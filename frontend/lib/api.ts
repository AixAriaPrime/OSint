const configuredApiUrl = process.env.NEXT_PUBLIC_API_URL?.trim();

export function getApiUrl(): string | null {
  if (configuredApiUrl) {
    return configuredApiUrl.replace(/\/+$/, "");
  }

  if (
    typeof window !== "undefined" &&
    (window.location.hostname === "localhost" || window.location.hostname === "******27.0.0.******")
  ) {
    return "http://localhost:8000";
  }

  return null;
}

export function getWebSocketUrl(apiUrl: string): string {
  return `${apiUrl.replace(/^http(s?)/, (_match, secure: string) => (secure ? "wss" : "ws"))}/ws`;
}
