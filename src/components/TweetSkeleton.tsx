// Tweet-shaped loading skeleton (Section 4C) — distinguishes "loading" from
// "frozen" on a slow connection, and previews the real card's layout.
export function TweetSkeleton() {
  return (
    <div
      aria-busy="true"
      aria-label="Loading tweet"
      className="mx-auto flex w-[500px] max-w-full animate-pulse flex-col gap-3 rounded-2xl border border-border bg-surface p-4"
    >
      <div className="flex items-center gap-2.5">
        <div className="h-10 w-10 rounded-full bg-zinc-200" />
        <div className="flex flex-col gap-1.5">
          <div className="h-3 w-30 rounded bg-zinc-200" />
          <div className="h-2.5 w-20 rounded bg-zinc-100" />
        </div>
      </div>
      <div className="h-3 w-full rounded bg-zinc-100" />
      <div className="h-3 w-[70%] rounded bg-zinc-100" />
    </div>
  );
}
