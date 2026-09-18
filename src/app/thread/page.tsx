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
    <main className="flex-1 pb-24 sm:pb-0">
      <div className="mx-auto max-w-[720px] px-4 pb-6 pt-16 text-center sm:px-6">
        <h1 className="mb-2 text-[28px] font-semibold leading-tight tracking-tight text-foreground">
          Turn a thread into one shareable image.
        </h1>
        <p className="mb-8 text-sm leading-relaxed text-text-secondary">
          Add each tweet in the thread, in order — manual, no auto-discovery
          (see README).
        </p>
        <div className="mx-auto flex max-w-[560px] gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAdd()}
            placeholder="https://x.com/user/status/..."
            className="flex-1 rounded-[10px] border border-border bg-surface px-4 py-3 text-sm outline-none focus:border-accent focus:ring-2 focus:ring-accent/40"
            aria-label="Tweet URL"
          />
          <button
            type="button"
            onClick={handleAdd}
            className="rounded-[10px] bg-accent px-5 py-3 text-sm font-semibold text-white hover:bg-accent-hover"
          >
            Add tweet
          </button>
        </div>
        {capMessage && (
          <p role="alert" className="mt-4 flex items-center justify-center gap-1.5 text-sm text-danger">
            <span aria-hidden="true">⚠</span>
            {capMessage}
          </p>
        )}
      </div>

      <div className="mx-auto grid max-w-[1180px] grid-cols-1 gap-6 px-4 pb-6 sm:px-6 sm:grid-cols-[1fr_340px]">
        <div className="flex w-full flex-col items-center gap-5 overflow-x-auto rounded-2xl border border-border bg-surface p-7">
          <ThreadBuilder
            ref={builderRef}
            style={style}
            initialIds={initialIds}
            onStateChange={handleThreadStateChange}
          />
          <div className="hidden sm:block">
            <ExportControls
              canvasRef={canvasRef}
              scale={style.scale}
              shareUrl={shareUrl}
              disabled={!threadState.canExport}
            />
          </div>
          {!threadState.canExport && threadState.ids.length > 0 && (
            <p className="text-xs text-text-secondary">
              Export is blocked until every tweet in the thread loads.
            </p>
          )}
        </div>
        <div className="self-start rounded-2xl border border-border bg-surface p-5">
          <CustomizePanel style={style} onChange={handleStyleChange} />
        </div>
      </div>

      <div className="fixed inset-x-0 bottom-0 border-t border-border bg-surface px-4 py-3 sm:hidden">
        <ExportControls
          canvasRef={canvasRef}
          scale={style.scale}
          shareUrl={shareUrl}
          disabled={!threadState.canExport}
        />
      </div>
    </main>
  );
}
