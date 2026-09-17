export type Theme = "light" | "dark";
export type Scale = 1 | 2 | 3;

export interface BackgroundPreset {
  id: string;
  label: string;
  css: string;
}

// D3: curated theme packs, not a raw color picker only.
export const BACKGROUND_PRESETS: BackgroundPreset[] = [
  { id: "twitter-blue", label: "Twitter Blue", css: "linear-gradient(135deg,#1d9bf0,#7856ff)" },
  { id: "sunset", label: "Sunset", css: "linear-gradient(135deg,#ff7e5f,#feb47b)" },
  { id: "midnight", label: "Midnight", css: "linear-gradient(135deg,#0f2027,#203a43,#2c5364)" },
  { id: "mint", label: "Mint", css: "linear-gradient(135deg,#43e97b,#38f9d7)" },
  { id: "plain-white", label: "Plain white", css: "#ffffff" },
  { id: "plain-black", label: "Plain black", css: "#000000" },
];

export interface StyleState {
  v: 1; // schema version (Section 2: 2D — versioned for graceful fallback)
  backgroundId: string;
  padding: number;
  scale: Scale;
  theme: Theme;
}

export const DEFAULT_STYLE: StyleState = {
  v: 1,
  backgroundId: "twitter-blue",
  padding: 48,
  scale: 2,
  theme: "light",
};

export function backgroundCss(id: string): string {
  return BACKGROUND_PRESETS.find((p) => p.id === id)?.css ?? BACKGROUND_PRESETS[0].css;
}

/**
 * Encodes style state into URL search params. Pure serialization — no
 * React, no DOM, no networking (eng review Section C module boundaries).
 */
export function encodeStyleState(tweetId: string, style: StyleState): string {
  const params = new URLSearchParams({
    id: tweetId,
    v: String(style.v),
    bg: style.backgroundId,
    p: String(style.padding),
    s: String(style.scale),
    t: style.theme,
  });
  return `?${params.toString()}`;
}

/**
 * Decodes URL search params back into style state. Defensive: any
 * corrupted, missing, or unrecognized field falls back to the default
 * rather than throwing or rendering broken (Section 2D). Returns null for
 * tweetId only when no id param is present at all.
 */
export function decodeStyleState(
  params: URLSearchParams,
): { tweetId: string | null; style: StyleState } {
  const tweetId = params.get("id");
  const v = Number(params.get("v"));

  if (v !== 1) {
    return { tweetId, style: DEFAULT_STYLE };
  }

  const bg = params.get("bg");
  const p = Number(params.get("p"));
  const s = Number(params.get("s"));
  const t = params.get("t");

  return {
    tweetId,
    style: {
      v: 1,
      backgroundId: bg && BACKGROUND_PRESETS.some((preset) => preset.id === bg) ? bg : DEFAULT_STYLE.backgroundId,
      padding: Number.isFinite(p) && p >= 0 && p <= 200 ? p : DEFAULT_STYLE.padding,
      scale: s === 1 || s === 2 || s === 3 ? (s as Scale) : DEFAULT_STYLE.scale,
      theme: t === "light" || t === "dark" ? t : DEFAULT_STYLE.theme,
    },
  };
}
