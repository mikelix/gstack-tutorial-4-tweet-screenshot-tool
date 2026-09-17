import { NextRequest, NextResponse } from "next/server";
import { fetchTweet, TwitterApiError } from "react-tweet/api";

export const dynamic = "force-dynamic";

const TWEET_ID = /^[0-9]{1,40}$/;
const UPSTREAM_TIMEOUT_MS = 8_000;

type ErrorBody = { error: string; code: string };

function errorResponse(code: string, message: string, status: number) {
  const body: ErrorBody = { error: message, code };
  return NextResponse.json(body, { status });
}

export async function GET(
  _request: NextRequest,
  ctx: RouteContext<"/api/tweet/[id]">,
) {
  const { id } = await ctx.params;

  if (!TWEET_ID.test(id)) {
    return errorResponse("invalid_id", "That doesn't look like a tweet link", 400);
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), UPSTREAM_TIMEOUT_MS);

  try {
    const result = await fetchWithOneRetry(id, controller.signal);
    clearTimeout(timeout);

    if (result.notFound) {
      return errorResponse("not_found", "Tweet not found, deleted, or protected", 404);
    }
    if (result.tombstone) {
      return errorResponse("protected", "This tweet is protected or private", 404);
    }
    if (!result.data) {
      // Defensive: react-tweet's success path guarantees one of
      // data/notFound/tombstone, but never trust an upstream contract
      // silently (eng review 2E — malformed upstream shape must not crash).
      console.warn("[tweet] upstream returned no data and no known flag", { id });
      return errorResponse("upstream_malformed", "Couldn't load this tweet — try again", 502);
    }

    return NextResponse.json(result.data, {
      headers: {
        // Short-TTL edge caching (CEO review 1B) — reduces redundant
        // upstream calls for the same viral tweet without going stale for
        // more than a couple minutes.
        "Cache-Control": "public, max-age=120, s-maxage=120, stale-while-revalidate=300",
      },
    });
  } catch (err) {
    clearTimeout(timeout);

    if (err instanceof Error && err.name === "AbortError") {
      return errorResponse("upstream_timeout", "Couldn't load this tweet — try again", 504);
    }
    if (err instanceof TwitterApiError) {
      if (err.status === 429) {
        return errorResponse(
          "upstream_rate_limited",
          "X is rate-limiting us — try again shortly",
          429,
        );
      }
      console.warn("[tweet] upstream server error", { id, status: err.status });
      return errorResponse("upstream_error", "Couldn't load this tweet — try again", 502);
    }
    console.warn("[tweet] unexpected error", { id, message: (err as Error).message });
    return errorResponse("unexpected", "Couldn't load this tweet — try again", 502);
  }
}

async function fetchWithOneRetry(id: string, signal: AbortSignal) {
  try {
    return await fetchTweet(id, { signal });
  } catch (err) {
    if (err instanceof Error && err.name === "AbortError") throw err;
    if (err instanceof TwitterApiError && err.status === 429) throw err;
    // One bounded retry for transient upstream failures only (timeout
    // already governed by the outer AbortController's single deadline).
    return await fetchTweet(id, { signal });
  }
}
