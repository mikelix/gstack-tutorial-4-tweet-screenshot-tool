import { NextRequest, NextResponse } from "next/server";
import {
  assertAllowedMediaUrl,
  MediaUrlRejectedError,
  PROXY_FETCH_TIMEOUT_MS,
  PROXY_MAX_RESPONSE_BYTES,
} from "@/lib/media-hosts";

export const dynamic = "force-dynamic";

const MAX_REDIRECTS = 3;

/**
 * Fetches url with redirects followed manually so every hop is re-validated
 * against the allowlist (eng review B2 — blind redirect-following is a
 * classic SSRF bypass: the initial URL can pass the allowlist while a
 * redirect target does not).
 */
async function fetchWithValidatedRedirects(
  rawUrl: string,
  signal: AbortSignal,
): Promise<Response> {
  let current = assertAllowedMediaUrl(rawUrl);
  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
    const res = await fetch(current.toString(), {
      redirect: "manual",
      signal,
      headers: { Accept: "image/*,video/*" },
    });

    if (res.status >= 300 && res.status < 400) {
      const location = res.headers.get("location");
      if (!location) {
        throw new MediaUrlRejectedError("redirect with no Location header");
      }
      if (hop === MAX_REDIRECTS) {
        throw new MediaUrlRejectedError("too many redirects");
      }
      // Resolve relative redirects against the current URL, then
      // re-validate the resolved target — this is the step a naive
      // "follow redirects automatically" implementation skips.
      current = assertAllowedMediaUrl(new URL(location, current).toString());
      continue;
    }

    return res;
  }
  throw new MediaUrlRejectedError("too many redirects");
}

export async function GET(request: NextRequest) {
  const url = request.nextUrl.searchParams.get("url");
  if (!url) {
    return NextResponse.json({ error: "missing url" }, { status: 400 });
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), PROXY_FETCH_TIMEOUT_MS);

  try {
    const upstream = await fetchWithValidatedRedirects(url, controller.signal);

    if (!upstream.ok) {
      console.warn("[image-proxy] upstream error", { status: upstream.status });
      return NextResponse.json({ error: "upstream error" }, { status: 502 });
    }

    const contentType = upstream.headers.get("content-type") ?? "";
    if (!contentType.startsWith("image/") && !contentType.startsWith("video/")) {
      console.warn("[image-proxy] rejected content-type", { contentType });
      return NextResponse.json({ error: "unexpected content type" }, { status: 502 });
    }

    const contentLength = upstream.headers.get("content-length");
    if (contentLength && Number(contentLength) > PROXY_MAX_RESPONSE_BYTES) {
      console.warn("[image-proxy] response too large", { contentLength });
      return NextResponse.json({ error: "response too large" }, { status: 502 });
    }

    const buf = await upstream.arrayBuffer();
    if (buf.byteLength > PROXY_MAX_RESPONSE_BYTES) {
      console.warn("[image-proxy] response exceeded cap after download", {
        bytes: buf.byteLength,
      });
      return NextResponse.json({ error: "response too large" }, { status: 502 });
    }

    return new NextResponse(buf, {
      status: 200,
      headers: {
        "Content-Type": contentType,
        // Twitter media URLs are content-addressed in practice; cache
        // aggressively at the edge (CEO review 1B's caching rationale
        // applies here too — same-origin proxy, no cookies/auth forwarded).
        "Cache-Control": "public, max-age=3600, s-maxage=86400",
      },
    });
  } catch (err) {
    if (err instanceof MediaUrlRejectedError) {
      console.warn("[image-proxy] rejected", { reason: err.reason });
      return NextResponse.json({ error: "rejected" }, { status: 400 });
    }
    if (err instanceof Error && err.name === "AbortError") {
      console.warn("[image-proxy] timeout");
      return NextResponse.json({ error: "timeout" }, { status: 504 });
    }
    console.warn("[image-proxy] unexpected error", { message: (err as Error).message });
    return NextResponse.json({ error: "proxy failed" }, { status: 502 });
  } finally {
    clearTimeout(timeout);
  }
}
