import { DEFAULT_STYLE, StyleState } from "@/lib/style-state";

// OV-4: hard cap on thread length so a shareable link never exceeds a
// safe cross-platform URL length. Enforced on Add, not silently truncated.
export const MAX_THREAD_LENGTH = 12;

export interface ThreadUrlState {
  ids: string[];
  style: StyleState;
}

/** Pure serialization — no React, no DOM, no networking. */
export function encodeThreadState(ids: string[], style: StyleState): string {
  const params = new URLSearchParams({
    ids: ids.join(","),
    v: String(style.v),
    bg: style.backgroundId,
    p: String(style.padding),
    s: String(style.scale),
    t: style.theme,
  });
  return `?${params.toString()}`;
}

/**
 * Defensive decode: any corrupted, missing, or unrecognized field falls
 * back to a default rather than throwing or rendering broken (Section 2D).
 * A malformed `ids` list degrades to an empty thread rather than crashing.
 */
export function decodeThreadState(params: URLSearchParams): ThreadUrlState {
  const rawIds = params.get("ids");
  const ids = rawIds
    ? rawIds
        .split(",")
        .map((s) => s.trim())
        .filter((s) => /^\d{1,40}$/.test(s))
        .slice(0, MAX_THREAD_LENGTH)
    : [];

  const v = Number(params.get("v"));
  if (v !== 1) {
    return { ids, style: DEFAULT_STYLE };
  }

  const bg = params.get("bg");
  const p = Number(params.get("p"));
  const s = Number(params.get("s"));
  const t = params.get("t");

  return {
    ids,
    style: {
      v: 1,
      backgroundId: bg ? bg : DEFAULT_STYLE.backgroundId,
      padding: Number.isFinite(p) && p >= 0 && p <= 200 ? p : DEFAULT_STYLE.padding,
      scale: s === 1 || s === 2 || s === 3 ? (s as StyleState["scale"]) : DEFAULT_STYLE.scale,
      theme: t === "light" || t === "dark" ? t : DEFAULT_STYLE.theme,
    },
  };
}
