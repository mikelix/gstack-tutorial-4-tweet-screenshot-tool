"use client";

import { useEffect, useRef, useState } from "react";
import type { Tweet } from "react-tweet/api";
import { TweetCanvas } from "@/components/TweetCanvas";
import { CustomizePanel } from "@/components/CustomizePanel";
import { ExportControls } from "@/components/ExportControls";
import { TweetSkeleton } from "@/components/TweetSkeleton";
import { parseTweetId } from "@/lib/tweet-url";
import { decodeStyleState, encodeStyleState, DEFAULT_STYLE, StyleState } from "@/lib/style-state";

type Status =
  | { phase: "idle" }
  | { phase: "loading" }
  | { phase: "loaded"; tweet: Tweet }
  | { phase: "error"; message: string };

/**
 * Canonical URL → state decoder (Phase 7 #2). The SAME function backs
 * initial page load and every `popstate` (back/forward) — there is no
 * second, divergent hydration path. Malformed/unknown values fall back to
 * defaults; an unrecognized schema version still preserves tweet identity
 * (Section 2D, exercised for real by Phase 7's back/forward requirement).
 * Never encodes fetched tweet data itself, only its id + style choices.
 */
function hydrateStateFromUrl(): { tweetId: string | null; style: StyleState } {
  if (typeof window === "undefined") return { tweetId: null, style: DEFAULT_STYLE };
  const params = new URLSearchParams(window.location.search);
  return decodeStyleState(params);
}

type HistoryMode = "push" | "replace" | "none";

export default function Home() {
  const [{ tweetId: initialTweetId, style: initialStyle }] = useState(hydrateStateFromUrl);
  const [input, setInput] = useState(initialTweetId ?? "");
  const [status, setStatus] = useState<Status>({ phase: "idle" });
  const [style, setStyle] = useState<StyleState>(initialStyle);
  const canvasRef = useRef<HTMLDivElement>(null);

  // Stale-response race protection (Section 4A): only the latest request's
  // response is ever applied; a superseded in-flight request is aborted
  // rather than left to resolve uselessly, and AbortError is treated as
  // normal control flow — never surfaced as a user-facing error.
  const requestRef = useRef<{ token: symbol; controller: AbortController } | null>(null);
  // Tracks which tweet id is currently loaded so popstate can skip a
  // redundant refetch when only style (not the tweet) changed.
  const loadedIdRef = useRef<string | null>(null);

  async function loadTweet(rawInput: string, historyMode: HistoryMode, styleForUrl?: StyleState) {
    const id = parseTweetId(rawInput);
    if (!id) {
      setStatus({ phase: "error", message: "That doesn't look like a tweet link" });
      return;
    }

    requestRef.current?.controller.abort();
    const token = Symbol("request");
    const controller = new AbortController();
    requestRef.current = { token, controller };

    setStatus({ phase: "loading" });

    try {
      const res = await fetch(`/api/tweet/${id}`, { signal: controller.signal });
      const body = await res.json();

      if (requestRef.current?.token !== token) return; // superseded by a newer request

      if (!res.ok) {
        setStatus({ phase: "error", message: body.error ?? "Couldn't load this tweet" });
        return;
      }
      setStatus({ phase: "loaded", tweet: body as Tweet });
      loadedIdRef.current = id;
      applyHistory(historyMode, encodeStyleState(id, styleForUrl ?? style));
    } catch (err) {
      if (requestRef.current?.token !== token) return;
      if (err instanceof Error && err.name === "AbortError") return; // normal control flow
      setStatus({ phase: "error", message: (err as Error).message });
    }
  }

  function applyHistory(mode: HistoryMode, url: string) {
    if (mode === "push") window.history.pushState(null, "", url);
    else if (mode === "replace") window.history.replaceState(null, "", url);
    // "none": the URL already reflects this state (initial load from a
    // shared link, or a popstate-driven restore) — never write it back.
  }

  // Fires the initial load (a real side effect: a network request) if a
  // shared link named a tweet id. The URL is already correct, so this
  // never pushes/replaces it. Initial style/input were already derived via
  // the lazy useState initializer above.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional: fire the network request a shared link named, not a derived-state loop
    if (initialTweetId) void loadTweet(initialTweetId, "none");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Phase 7 #3: browser Back/Forward. Re-runs the SAME hydration function
  // used on initial load. Never calls pushState/replaceState from here —
  // the URL the browser just navigated to is already the source of truth,
  // so writing it back would be a no-op at best and a loop risk at worst.
  useEffect(() => {
    function onPopState() {
      const { tweetId, style: hydratedStyle } = hydrateStateFromUrl();
      setStyle(hydratedStyle);
      if (tweetId) {
        setInput(tweetId);
        if (tweetId !== loadedIdRef.current) {
          void loadTweet(tweetId, "none");
        }
      } else {
        setStatus({ phase: "idle" });
        loadedIdRef.current = null;
      }
    }
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
    // loadTweet is intentionally omitted: registered once on mount, and
    // every call site here passes historyMode="none", so the only closed-
    // over value loadTweet reads for URL-writing (`style`) is never used —
    // a stale closure of it is inert for this effect specifically.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSubmit() {
    void loadTweet(input, "push");
  }

  function handleStyleChange(next: StyleState) {
    // Continuous input (the padding slider) replaces the current history
    // entry so dragging doesn't flood back/forward with one entry per
    // pixel; discrete choices (background/scale/theme) push a new entry
    // so Back/Forward has something meaningful to restore between.
    const isContinuousOnly =
      next.backgroundId === style.backgroundId &&
      next.scale === style.scale &&
      next.theme === style.theme &&
      next.padding !== style.padding;

    setStyle(next);
    if (status.phase === "loaded") {
      applyHistory(
        isContinuousOnly ? "replace" : "push",
        encodeStyleState(status.tweet.id_str, next),
      );
    }
  }

  const shareUrl =
    typeof window !== "undefined" && status.phase === "loaded"
      ? `${window.location.origin}${encodeStyleState(status.tweet.id_str, style)}`
      : "";

  return (
    <main style={{ padding: 24, maxWidth: 900, margin: "0 auto", fontFamily: "system-ui" }}>
      <h1 style={{ fontSize: 22 }}>Tweet Screenshot</h1>
      <p style={{ color: "#666" }}>Paste a tweet link, customize it, export a PNG.</p>

      <div style={{ display: "flex", gap: 8, margin: "16px 0" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          placeholder="https://x.com/user/status/..."
          style={{ flex: 1, padding: 8 }}
          aria-label="Tweet URL"
        />
        <button type="button" onClick={handleSubmit} disabled={status.phase === "loading"}>
          Load
        </button>
      </div>

      {status.phase === "error" && (
        <p role="alert" style={{ color: "crimson" }}>
          {status.message}
        </p>
      )}

      {status.phase === "loading" && <TweetSkeleton />}

      {status.phase === "loaded" && (
        <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
          <div>
            <TweetCanvas ref={canvasRef} tweet={status.tweet} style={style} />
            <div style={{ marginTop: 16 }}>
              <ExportControls
                canvasRef={canvasRef}
                scale={style.scale}
                shareUrl={shareUrl}
                disabled={false}
              />
            </div>
          </div>
          <CustomizePanel style={style} onChange={handleStyleChange} />
        </div>
      )}
    </main>
  );
}
