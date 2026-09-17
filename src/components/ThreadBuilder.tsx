"use client";

import { forwardRef, useCallback, useEffect, useId, useImperativeHandle, useRef, useState } from "react";
import type { Tweet } from "react-tweet/api";
import { TweetCanvas } from "@/components/TweetCanvas";
import { parseTweetId } from "@/lib/tweet-url";
import { StyleState, backgroundCss } from "@/lib/style-state";
import { MAX_THREAD_LENGTH } from "@/lib/thread-state";

interface ThreadItem {
  key: string;
  tweetId: string;
  status: "loading" | "loaded" | "error";
  tweet?: Tweet;
  error?: string;
}

export interface ThreadBuilderHandle {
  addTweet: (rawInput: string) => void;
  /** The outer stacking container — the only thing ExportPipeline needs; it never inspects individual items. */
  getContainerElement: () => HTMLDivElement | null;
}

export interface ThreadBuilderProps {
  style: StyleState;
  initialIds?: string[];
  onStateChange: (state: { ids: string[]; canExport: boolean }) => void;
}

/**
 * Owns the thread item list: independent fetch-per-item, order, duplicate
 * prevention, retry, remove. Does NOT own export mechanics or URL
 * serialization (eng review Section C) — reports state changes upward via
 * onStateChange so the page can update those separately.
 *
 * Composes unmodified TweetCanvas instances inside its own stacking
 * container; TweetCanvas itself stays entirely unaware it's part of a
 * thread (confirms the OV-7 hypothesis — see plan Section "Re-evaluate the
 * component-sharing hypothesis").
 */
export const ThreadBuilder = forwardRef<ThreadBuilderHandle, ThreadBuilderProps>(
  function ThreadBuilder({ style, initialIds = [], onStateChange }, exportRef) {
    const [items, setItems] = useState<ThreadItem[]>([]);
    const idPrefix = useId();
    const nextKey = useRef(0);
    const hydratedRef = useRef(false);
    const containerRef = useRef<HTMLDivElement>(null);

    async function fetchItem(key: string, tweetId: string) {
      setItems((prev) => prev.map((it) => (it.key === key ? { ...it, status: "loading" } : it)));
      try {
        const res = await fetch(`/api/tweet/${tweetId}`);
        const body = await res.json();
        setItems((prev) =>
          prev.map((it) =>
            it.key === key
              ? res.ok
                ? { ...it, status: "loaded", tweet: body as Tweet, error: undefined }
                : { ...it, status: "error", error: body.error ?? "Couldn't load this tweet" }
              : it,
          ),
        );
      } catch (err) {
        setItems((prev) =>
          prev.map((it) =>
            it.key === key ? { ...it, status: "error", error: (err as Error).message } : it,
          ),
        );
      }
    }

    const addTweet = useCallback((rawInput: string) => {
      const tweetId = parseTweetId(rawInput);
      if (!tweetId) return;

      setItems((prev) => {
        if (prev.length >= MAX_THREAD_LENGTH) return prev; // caller shows the cap message
        if (prev.some((it) => it.tweetId === tweetId)) return prev; // duplicate prevention
        const key = `${idPrefix}-${nextKey.current++}`;
        void fetchItem(key, tweetId);
        return [...prev, { key, tweetId, status: "loading" }];
      });
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useImperativeHandle(
      exportRef,
      () => ({ addTweet, getContainerElement: () => containerRef.current }),
      [addTweet],
    );

    // Hydrate from a shared thread link once, on mount.
    useEffect(() => {
      if (hydratedRef.current) return;
      hydratedRef.current = true;
      for (const id of initialIds) addTweet(id);
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    function removeItem(key: string) {
      setItems((prev) => prev.filter((it) => it.key !== key));
    }

    function moveItem(key: string, direction: -1 | 1) {
      setItems((prev) => {
        const index = prev.findIndex((it) => it.key === key);
        const target = index + direction;
        if (index === -1 || target < 0 || target >= prev.length) return prev;
        const next = [...prev];
        [next[index], next[target]] = [next[target], next[index]];
        return next;
      });
    }

    function retryItem(key: string) {
      const item = items.find((it) => it.key === key);
      if (item) void fetchItem(key, item.tweetId);
    }

    // Report upward: current tweet ids (order-preserving, for URL state)
    // and whether export should be blocked — never silently omit a failed
    // tweet from the thread, block export until it's resolved or removed.
    useEffect(() => {
      onStateChange({
        ids: items.map((it) => it.tweetId),
        canExport: items.length > 0 && items.every((it) => it.status === "loaded"),
      });
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [items]);

    return (
      <div
        ref={containerRef}
        id={idPrefix}
        style={{ display: "inline-block", background: backgroundCss(style.backgroundId), padding: style.padding }}
        data-theme={style.theme}
      >
        {items.length === 0 && (
          <p style={{ color: "white", margin: 0, minWidth: 300 }}>Add your first tweet to start a thread.</p>
        )}
        {items.map((item, index) => (
          <div key={item.key} style={{ marginBottom: index < items.length - 1 ? 12 : 0 }}>
            {item.status === "loading" && (
              <div
                aria-busy="true"
                style={{ width: 500, maxWidth: "100%", height: 120, background: "#eee", borderRadius: 16 }}
              />
            )}
            {item.status === "error" && (
              <div
                role="alert"
                style={{
                  width: 500,
                  maxWidth: "100%",
                  border: "1px solid crimson",
                  borderRadius: 16,
                  padding: 16,
                  background: "white",
                }}
              >
                <p>Couldn&apos;t load this tweet: {item.error}</p>
                <button type="button" onClick={() => retryItem(item.key)}>
                  Retry
                </button>{" "}
                <button type="button" onClick={() => removeItem(item.key)}>
                  Remove
                </button>
              </div>
            )}
            {item.status === "loaded" && item.tweet && (
              <div>
                <TweetCanvas tweet={item.tweet} style={{ ...style, backgroundId: "plain-white", padding: 16 }} />
                {/* data-export-hide: stripped from the CLONE before capture
                    (export-image.ts) — these controls must never appear in
                    the exported PNG, only in the live editing UI. */}
                <div data-export-hide="true" style={{ display: "flex", gap: 8, marginTop: 4 }}>
                  <button type="button" onClick={() => moveItem(item.key, -1)} disabled={index === 0} aria-label="Move up">
                    ↑
                  </button>
                  <button
                    type="button"
                    onClick={() => moveItem(item.key, 1)}
                    disabled={index === items.length - 1}
                    aria-label="Move down"
                  >
                    ↓
                  </button>
                  <button type="button" onClick={() => removeItem(item.key)}>
                    Remove
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    );
  },
);
