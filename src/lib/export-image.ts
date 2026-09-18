import { domToPng, domToBlob } from "modern-screenshot";
import { ALLOWED_MEDIA_HOSTS } from "@/lib/media-hosts";

/**
 * Capture-time asset fetcher for modern-screenshot. Runs only during
 * export, never affects the live on-screen preview: react-tweet's <img>/
 * <video> tags keep pointing at real twimg.com URLs (fine for display,
 * CORS only matters when the canvas later tries to READ pixel data).
 *
 * For allowlisted Twitter media hosts, routes the fetch through our
 * same-origin /api/image-proxy so the browser gets a same-origin response
 * it can safely read into the canvas. Everything else falls through to
 * modern-screenshot's normal fetch (returning false).
 */
async function proxyAwareFetch(url: string): Promise<string | false> {
  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    return false;
  }

  if (!ALLOWED_MEDIA_HOSTS.has(parsed.hostname)) {
    return false;
  }

  const res = await fetch(`/api/image-proxy?url=${encodeURIComponent(url)}`);
  if (!res.ok) {
    // Fail the individual asset, not the whole capture — let
    // modern-screenshot's own timeout/placeholder handling take over.
    return false;
  }
  const blob = await res.blob();
  // modern-screenshot's fetchFn contract expects a result shaped like its
  // own `responseType: "dataUrl"` fetch (verified against
  // node_modules/modern-screenshot/dist/index.mjs:1135-1244 — the cloned
  // DOM gets serialized to an SVG string and re-loaded as a fresh image
  // resource, where a blob: URL created in the live document does not
  // reliably resolve; a self-contained base64 data: URL does).
  return await blobToDataUrl(blob);
}

function blobToDataUrl(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(blob);
  });
}

/**
 * Removes anything marked data-export-hide from the CLONE only (e.g.
 * ThreadBuilder's per-item reorder/remove controls) — never affects the
 * live interactive UI, only what gets rasterized.
 */
function stripExportHiddenElements(cloned: Node) {
  if (!(cloned instanceof HTMLElement)) return;
  if (cloned.dataset.exportHide === "true") {
    cloned.remove();
    return;
  }
  cloned.querySelectorAll<HTMLElement>("[data-export-hide]").forEach((el) => el.remove());
}

/**
 * Swaps any cloned <video> element for an <img> pointing at its poster
 * frame (OV-3: deterministic export instead of whatever frame happened to
 * be painted). Reads the real `poster` attribute react-tweet's
 * TweetMediaVideo already sets — no separate media-URL lookup needed.
 */
function replaceVideoWithPosterImage(cloned: Node) {
  stripExportHiddenElements(cloned);
  if (!(cloned instanceof HTMLElement)) return;
  const videos = cloned.matches("video")
    ? [cloned]
    : Array.from(cloned.querySelectorAll("video"));

  for (const video of videos) {
    const poster = video.getAttribute("poster");
    const img = document.createElement("img");
    img.className = video.className;
    if (poster) img.src = poster;
    img.setAttribute("data-export-video-poster", "true");
    // A small play-icon badge so a static export of a video tweet reads
    // as intentional, not broken (OV-3).
    const badge = document.createElement("div");
    badge.setAttribute("data-export-video-badge", "true");
    badge.style.cssText =
      "position:absolute;inset:0;display:flex;align-items:center;justify-content:center;";
    badge.innerHTML =
      '<svg width="48" height="48" viewBox="0 0 24 24" fill="white" style="filter:drop-shadow(0 1px 3px rgba(0,0,0,.6))"><circle cx="12" cy="12" r="12" fill="rgba(0,0,0,.45)"/><path d="M10 8l6 4-6 4V8z" fill="white"/></svg>';
    const wrapper = document.createElement("div");
    wrapper.style.cssText = "position:relative;display:inline-block;width:100%;";
    video.replaceWith(wrapper);
    wrapper.appendChild(img);
    wrapper.appendChild(badge);
  }
}

/**
 * Runs a capture function against a sanitized OFF-SCREEN CLONE of `node`,
 * never the live node itself.
 *
 * Root cause (measured, not guessed): modern-screenshot's own internal
 * video handling (`cloneVideo`) sets `cloned.currentTime = video.currentTime`
 * and awaits a `seeked` event before it will proceed. Our `<video>` elements
 * are never played, so `currentTime` is already `0` — setting it to `0`
 * again does not fire `seeked` in Chromium, so that await never resolves.
 * This happens inside modern-screenshot's OWN clone step, before our
 * `onCloneNode` hook ever runs, so `onCloneNode` can't prevent it — it was
 * already too late. Measured: single video tweet, thread with 2 video
 * tweets, and a thread with quoted-tweet video all hang identically, with
 * zero asset-proxy fetches ever firing, at any scale, even with a 60s
 * timeout (see docs/design-review-4.1 investigation notes).
 *
 * The fix is to never let modern-screenshot see a real `<video>` element:
 * clone `node` ourselves, swap every `<video>` for its poster `<img>` synchronously
 * on that clone (existing `replaceVideoWithPosterImage`, now applied before
 * capture instead of via `onCloneNode`), and only then hand the clone to
 * domToPng/domToBlob. The clone is attached off-screen (not `display:none`)
 * so layout/computed styles resolve the same as the live node.
 */
async function withSanitizedClone<T>(
  node: HTMLElement,
  run: (clone: HTMLElement) => Promise<T>,
): Promise<T> {
  const clone = node.cloneNode(true) as HTMLElement;
  clone.style.position = "fixed";
  clone.style.top = "0";
  clone.style.left = "-99999px";
  clone.style.pointerEvents = "none";
  clone.setAttribute("aria-hidden", "true");
  document.body.appendChild(clone);
  try {
    replaceVideoWithPosterImage(clone);
    return await run(clone);
  } finally {
    clone.remove();
  }
}

export interface CaptureOptions {
  scale?: number;
  timeoutMs?: number;
}

export interface CaptureResult {
  dataUrl: string;
  width: number;
  height: number;
}

/**
 * Waits for fonts + images to finish loading and applies a capture
 * timeout, shared by both the PNG (download/preview) and Blob (clipboard)
 * capture paths so the correctness gate (Phase 6) can't drift between them.
 */
async function withCaptureGate<T>(
  node: HTMLElement,
  { timeoutMs = 8_000 }: Pick<CaptureOptions, "timeoutMs">,
  run: (signal: AbortSignal) => Promise<T>,
): Promise<T> {
  if (node.offsetWidth === 0 || node.offsetHeight === 0) {
    throw new Error("Export target has zero dimensions");
  }

  await document.fonts.ready;

  const images = Array.from(node.querySelectorAll("img"));
  await Promise.all(
    images.map((img) =>
      img.complete
        ? Promise.resolve()
        : new Promise<void>((resolve) => {
            img.addEventListener("load", () => resolve(), { once: true });
            img.addEventListener("error", () => resolve(), { once: true });
          }),
    ),
  );

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await Promise.race([
      run(controller.signal),
      new Promise<never>((_, reject) => {
        controller.signal.addEventListener("abort", () =>
          reject(new Error("Export timed out — try a lower scale")),
        );
      }),
    ]);
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * Export correctness gate (Phase 6) for the download/preview path: waits
 * for fonts + images, applies a capture timeout, uses the verified
 * media-proxy path, and makes video export deterministic via the
 * poster-frame swap.
 */
export async function captureNodeToPng(
  node: HTMLElement,
  options: CaptureOptions = {},
): Promise<CaptureResult> {
  const scale = options.scale ?? 1;
  const dataUrl = await withCaptureGate(node, options, () =>
    withSanitizedClone(node, (clone) =>
      domToPng(clone, {
        scale,
        fetchFn: proxyAwareFetch,
      }),
    ),
  );
  return {
    dataUrl,
    width: Math.round(node.offsetWidth * scale),
    height: Math.round(node.offsetHeight * scale),
  };
}

/**
 * Export correctness gate for the clipboard path. Returns a Blob-producing
 * Promise intended to be handed DIRECTLY to `new ClipboardItem({...})`
 * without being awaited first (OV-2: Safari/iOS requires
 * `navigator.clipboard.write()` to be called synchronously within the
 * click handler's gesture chain — awaiting this function's result before
 * calling `clipboard.write()` breaks that chain and throws
 * `NotAllowedError` even with permission granted).
 */
export async function captureNodeToBlob(
  node: HTMLElement,
  options: CaptureOptions = {},
): Promise<Blob> {
  const scale = options.scale ?? 1;
  const blob = await withCaptureGate(node, options, () =>
    withSanitizedClone(node, (clone) =>
      domToBlob(clone, {
        scale,
        fetchFn: proxyAwareFetch,
      }),
    ),
  );
  if (!blob) throw new Error("Capture produced no image data");
  return blob;
}
