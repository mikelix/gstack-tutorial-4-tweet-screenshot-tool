const TWEET_URL = /^https?:\/\/(?:www\.)?(?:twitter|x)\.com\/[^/]+\/status(?:es)?\/(\d{1,40})/i;
const BARE_ID = /^\d{1,40}$/;

/**
 * Extracts a numeric tweet ID from a pasted URL, or accepts a bare numeric
 * ID directly. Returns null for anything else (Section 2: UrlParseError —
 * rejected before any request fires, no exception thrown).
 */
export function parseTweetId(input: string): string | null {
  const trimmed = input.trim();
  if (BARE_ID.test(trimmed)) return trimmed;
  const match = trimmed.match(TWEET_URL);
  return match ? match[1] : null;
}
