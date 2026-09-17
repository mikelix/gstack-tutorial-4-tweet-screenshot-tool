/**
 * Exact-match allowlist for X/Twitter's media CDN hosts. Never use
 * substring/suffix matching here — `url.includes('twimg.com')` would let
 * `evil-twimg.com.attacker.net` through (eng review B2).
 */
export const ALLOWED_MEDIA_HOSTS = new Set([
  "pbs.twimg.com",
  "abs.twimg.com",
  "video.twimg.com",
]);

export const PROXY_MAX_RESPONSE_BYTES = 10 * 1024 * 1024; // 10MB (B2)
export const PROXY_FETCH_TIMEOUT_MS = 8_000;

export class MediaUrlRejectedError extends Error {
  constructor(public reason: string) {
    super(`Rejected media URL: ${reason}`);
    this.name = "MediaUrlRejectedError";
  }
}

/**
 * Validates a candidate media URL against the allowlist. Throws
 * MediaUrlRejectedError with a specific reason on any violation so callers
 * can log why a request was rejected (eng review B2: exact host match,
 * https-only; redirect targets must be re-validated with this same
 * function, never assumed safe because the initial URL passed).
 */
export function assertAllowedMediaUrl(rawUrl: string): URL {
  let parsed: URL;
  try {
    parsed = new URL(rawUrl);
  } catch {
    throw new MediaUrlRejectedError("not a valid absolute URL");
  }

  if (parsed.protocol !== "https:") {
    throw new MediaUrlRejectedError(`protocol must be https, got ${parsed.protocol}`);
  }

  if (!ALLOWED_MEDIA_HOSTS.has(parsed.hostname)) {
    throw new MediaUrlRejectedError(`host not allowlisted: ${parsed.hostname}`);
  }

  return parsed;
}
