"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Design Review 4.1, Direction A: the shared header shell. Rendered from
 * layout.tsx so both routes get it for free — this is what fixes the
 * current-state finding that Thread mode has no navigation path from the
 * single-tweet page (docs/DESIGN_REVIEW_4_1_CURRENT_STATE.md).
 *
 * Presentation only: owns no tweet/style/export state.
 */
export function AppHeader() {
  const pathname = usePathname();
  const isThread = pathname?.startsWith("/thread") ?? false;

  return (
    <header className="border-b border-border bg-surface">
      <div className="mx-auto flex max-w-[1180px] items-center justify-between gap-3 px-4 py-2.5 sm:px-6">
        <Link
          href="/"
          aria-label="Tweet Screenshot — home"
          className="flex shrink-0 items-center gap-2 text-[15px] font-semibold text-foreground"
        >
          <span className="h-[22px] w-[22px] shrink-0 rounded-md bg-accent" aria-hidden="true" />
          <span className="hidden sm:inline" aria-hidden="true">Tweet Screenshot</span>
        </Link>
        <nav aria-label="Mode" className="flex shrink-0 gap-0.5 whitespace-nowrap rounded-lg bg-zinc-100 p-0.5">
          <Link
            href="/"
            aria-current={!isThread ? "page" : undefined}
            className={`rounded-md px-2.5 py-1.5 text-[13px] font-medium sm:px-3.5 ${
              !isThread ? "bg-white text-foreground shadow-sm" : "text-text-secondary"
            }`}
          >
            Single Tweet
          </Link>
          <Link
            href="/thread"
            aria-current={isThread ? "page" : undefined}
            className={`rounded-md px-2.5 py-1.5 text-[13px] font-medium sm:px-3.5 ${
              isThread ? "bg-white text-foreground shadow-sm" : "text-text-secondary"
            }`}
          >
            Thread
          </Link>
        </nav>
        <a
          href="https://github.com/mikelix/gstack-tutorial-4-tweet-screenshot-tool"
          className="hidden shrink-0 text-[13px] text-text-secondary hover:text-foreground sm:inline"
        >
          GitHub
        </a>
      </div>
    </header>
  );
}
