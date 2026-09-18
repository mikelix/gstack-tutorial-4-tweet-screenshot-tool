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

  // Design Review 4.1, Phase 6: a safe, neutral, non-controversial example
  // (the first tweet ever posted) so a new visitor can see real output
  // without hunting for a tweet of their own first. Reuses loadTweet
  // exactly as a manual paste would -- no separate code path.
  function handleTryExample() {
    const exampleUrl = "https://twitter.com/jack/status/20";
    setInput(exampleUrl);
    void loadTweet(exampleUrl, "push");
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

  const isEmpty = status.phase === "idle" || status.phase === "error";

  return (
    <main className="flex-1">
      {isEmpty && (
        <div className="mx-auto max-w-[720px] px-4 pb-10 pt-24 text-center sm:px-6">
          <h1 className="mb-3.5 text-[38px] font-semibold leading-[1.15] tracking-tight text-foreground">
            Turn any tweet into a beautiful image.
          </h1>
          <p className="mb-10 text-base leading-relaxed text-text-secondary">
            Paste an X link, customize the look, and export a high-resolution PNG.
          </p>
          <div className="mx-auto flex max-w-[560px] gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              placeholder="https://x.com/user/status/..."
              className="flex-1 rounded-[10px] border border-border bg-surface px-4 py-3.5 text-sm outline-none focus:border-accent focus:ring-2 focus:ring-accent/40"
              aria-label="Tweet URL"
            />
            <button
              type="button"
              onClick={handleSubmit}
              className="rounded-[10px] bg-accent px-5.5 py-3.5 text-sm font-semibold text-white hover:bg-accent-hover disabled:opacity-60"
            >
              Create
            </button>
          </div>
          <div className="mt-3.5">
            <button
              type="button"
              onClick={handleTryExample}
              className="text-sm font-medium text-accent hover:underline"
            >
              Try an example instead →
            </button>
          </div>

          {status.phase === "error" && (
            <p role="alert" className="mt-6 flex items-center justify-center gap-1.5 text-sm text-danger">
              <span aria-hidden="true">⚠</span>
              {status.message}
            </p>
          )}
        </div>
      )}

      {status.phase === "loading" && (
        <div className="mx-auto max-w-[1180px] px-4 pt-6 sm:px-6">
          <TweetSkeleton />
        </div>
      )}

      {status.phase === "loaded" && (
        <>
          <div className="mx-auto flex max-w-[1180px] items-center gap-2 px-4 pt-4 sm:px-6">
            <div className="flex flex-1 items-center gap-2 rounded-lg border border-border bg-surface px-3.5 py-2.5 focus-within:border-accent focus-within:ring-2 focus-within:ring-accent/40">
              <svg
                aria-hidden="true"
                viewBox="0 0 20 20"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.6"
                className="h-4 w-4 shrink-0 text-text-secondary"
              >
                <path d="M8.5 11.5a3 3 0 0 0 4.24 0l2.5-2.5a3 3 0 1 0-4.24-4.24l-1 1" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M11.5 8.5a3 3 0 0 0-4.24 0l-2.5 2.5a3 3 0 1 0 4.24 4.24l1-1" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
                placeholder="https://x.com/user/status/..."
                className="flex-1 bg-transparent text-[13px] text-text-secondary outline-none"
                aria-label="Tweet URL"
              />
            </div>
            <button
              type="button"
              onClick={handleSubmit}
              className="flex shrink-0 items-center gap-1.5 rounded-lg border border-border bg-surface px-4 py-2.5 text-[13px] font-medium text-foreground hover:border-accent hover:text-accent"
            >
              <svg aria-hidden="true" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6" className="h-3.5 w-3.5 shrink-0">
                <path d="M4 10a6 6 0 0 1 10.24-4.24M16 10a6 6 0 0 1-10.24 4.24" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M14 3v3h-3M6 17v-3h3" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <span className="hidden sm:inline">Load a different tweet</span>
              <span className="sm:hidden">Change</span>
            </button>
          </div>

          <div className="mx-auto grid max-w-[1180px] grid-cols-1 gap-6 px-4 pb-24 pt-6 sm:px-6 sm:pb-6 sm:grid-cols-[1fr_340px]">
            {/* overflow-x-auto is the safety net for the confirmed mobile
                overflow bug (docs/DESIGN_REVIEW_4_1_CURRENT_STATE.md):
                react-tweet's card has an intrinsic min-width wider than a
                375px viewport, so the card scrolls within its own
                container instead of blowing out the page. */}
            <div className="flex w-full flex-col items-center gap-5 overflow-x-auto rounded-2xl border border-border bg-surface p-7">
              <TweetCanvas ref={canvasRef} tweet={status.tweet} style={style} />
              <div className="hidden sm:block">
                <ExportControls
                  canvasRef={canvasRef}
                  scale={style.scale}
                  shareUrl={shareUrl}
                  disabled={false}
                />
              </div>
            </div>
            <div className="self-start rounded-2xl border border-border bg-surface p-5">
              <CustomizePanel style={style} onChange={handleStyleChange} />
            </div>
          </div>

          {/* Mobile: the same ExportControls instance, repositioned as a
              sticky bottom bar so Download PNG stays reachable without
              scrolling back up (Direction A mobile spec). */}
          <div className="fixed inset-x-0 bottom-0 border-t border-border bg-surface px-4 py-3 sm:hidden">
            <ExportControls
              canvasRef={canvasRef}
              scale={style.scale}
              shareUrl={shareUrl}
              disabled={false}
            />
          </div>
        </>
      )}
    </main>
  );
}
