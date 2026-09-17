"use client";

import { useEffect, useRef, useState } from "react";
import { ThreadBuilder, ThreadBuilderHandle } from "@/components/ThreadBuilder";
import { CustomizePanel } from "@/components/CustomizePanel";
import { ExportControls } from "@/components/ExportControls";
import { DEFAULT_STYLE, StyleState } from "@/lib/style-state";
import { decodeThreadState, encodeThreadState, MAX_THREAD_LENGTH } from "@/lib/thread-state";

function hydrateStateFromUrl() {
  if (typeof window === "undefined") return { ids: [] as string[], style: DEFAULT_STYLE };
  return decodeThreadState(new URLSearchParams(window.location.search));
}

export default function ThreadPage() {
  const [{ ids: initialIds, style: initialStyle }] = useState(hydrateStateFromUrl);
  const [input, setInput] = useState("");
  const [style, setStyle] = useState<StyleState>(initialStyle);
  const [threadState, setThreadState] = useState({ ids: [] as string[], canExport: false });
  const [capMessage, setCapMessage] = useState<string | null>(null);
  const builderRef = useRef<ThreadBuilderHandle>(null);
  // Kept in sync after every render (items changing, style changing, etc.)
  // rather than attached via a JSX `ref` — the export target here is
  // ThreadBuilder's internal container, reached only through its
  // imperative handle (eng review Section C: ExportPipeline needs just
  // the outer DOM node, nothing thread-specific).
  const canvasRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    canvasRef.current = builderRef.current?.getContainerElement() ?? null;
  });

  function handleAdd() {
    if (threadState.ids.length >= MAX_THREAD_LENGTH) {
      setCapMessage(`Threads longer than ${MAX_THREAD_LENGTH} tweets can't be shared as a link yet.`);
      return;
    }
    setCapMessage(null);
    builderRef.current?.addTweet(input);
    setInput("");
  }

  function handleThreadStateChange(next: { ids: string[]; canExport: boolean }) {
    setThreadState(next);
  }

  function handleStyleChange(next: StyleState) {
    setStyle(next);
  }

  // URL sync lives in ONE effect keyed off the current, authoritative
  // values (threadState.ids, style) — not threaded through callback
  // closures, which previously caused a stale-closure bug (see TODOS.md).
  useEffect(() => {
    // Guard: if a shared link named ids but ThreadBuilder hasn't finished
    // hydrating them into threadState yet, don't briefly overwrite the URL
    // with an empty ids list.
    if (initialIds.length > 0 && threadState.ids.length === 0) return;
    window.history.replaceState(null, "", encodeThreadState(threadState.ids, style));
  }, [threadState.ids, style, initialIds.length]);

  // Phase 7 pattern reused: popstate re-hydrates via the same decoder used
  // on initial load. Thread membership changes (add/remove/reorder) aren't
  // meaningfully "back"-able the way single-tweet navigation is, so this
  // page uses replaceState throughout rather than pushState — avoids a
  // history entry per reorder click while still keeping the URL shareable.
  useEffect(() => {
    function onPopState() {
      const { style: hydratedStyle } = hydrateStateFromUrl();
      setStyle(hydratedStyle);
    }
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  const shareUrl =
    typeof window !== "undefined"
      ? `${window.location.origin}${encodeThreadState(threadState.ids, style)}`
      : "";

  return (
    <main style={{ padding: 24, maxWidth: 900, margin: "0 auto", fontFamily: "system-ui" }}>
      <h1 style={{ fontSize: 22 }}>Thread Screenshot</h1>
      <p style={{ color: "#666" }}>
        Add each tweet in the thread, in order. Manual — no auto-discovery (see README).
      </p>

      <div style={{ display: "flex", gap: 8, margin: "16px 0" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAdd()}
          placeholder="https://x.com/user/status/..."
          style={{ flex: 1, padding: 8 }}
          aria-label="Tweet URL"
        />
        <button type="button" onClick={handleAdd}>
          Add tweet
        </button>
      </div>

      {capMessage && (
        <p role="alert" style={{ color: "crimson" }}>
          {capMessage}
        </p>
      )}

      <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
        <div>
          <ThreadBuilder
            ref={builderRef}
            style={style}
            initialIds={initialIds}
            onStateChange={handleThreadStateChange}
          />
          <div style={{ marginTop: 16 }}>
            <ExportControls
              canvasRef={canvasRef}
              scale={style.scale}
              shareUrl={shareUrl}
              disabled={!threadState.canExport}
            />
            {!threadState.canExport && threadState.ids.length > 0 && (
              <p style={{ color: "#666" }}>Export is blocked until every tweet in the thread loads.</p>
            )}
          </div>
        </div>
        <CustomizePanel style={style} onChange={handleStyleChange} />
      </div>
    </main>
  );
}
