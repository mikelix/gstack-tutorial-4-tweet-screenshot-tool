"use client";

import { RefObject, useState } from "react";
import { captureNodeToBlob, captureNodeToPng } from "@/lib/export-image";
import { Scale } from "@/lib/style-state";

export interface ExportControlsProps {
  canvasRef: RefObject<HTMLDivElement | null>;
  scale: Scale;
  shareUrl: string;
  disabled: boolean;
}

type ActionStatus = "idle" | "busy" | "done" | "error";

const clipboardSupported =
  typeof navigator !== "undefined" &&
  typeof navigator.clipboard !== "undefined" &&
  typeof window !== "undefined" &&
  typeof window.ClipboardItem !== "undefined";

export function ExportControls({ canvasRef, scale, shareUrl, disabled }: ExportControlsProps) {
  const [downloadStatus, setDownloadStatus] = useState<ActionStatus>("idle");
  const [copyStatus, setCopyStatus] = useState<ActionStatus>("idle");
  const [linkStatus, setLinkStatus] = useState<ActionStatus>("idle");
  const [message, setMessage] = useState<string | null>(null);

  async function handleDownload() {
    const node = canvasRef.current;
    if (!node) return;
    setDownloadStatus("busy");
    setMessage(null);
    try {
      const { dataUrl } = await captureNodeToPng(node, { scale });
      const a = document.createElement("a");
      a.href = dataUrl;
      a.download = "tweet.png";
      a.click();
      setDownloadStatus("done");
    } catch (err) {
      setDownloadStatus("error");
      setMessage((err as Error).message);
    }
  }

  function handleCopy() {
    const node = canvasRef.current;
    if (!node) return;
    setCopyStatus("busy");
    setMessage(null);

    if (!clipboardSupported) {
      // Feature-detected fallback: no clipboard image support, go straight
      // to download instead of attempting and failing.
      handleDownload().then(() => {
        setCopyStatus("done");
        setMessage("Clipboard image copy isn't supported in this browser — downloaded instead.");
      });
      return;
    }

    // Deliberately NOT awaited before clipboard.write() — the promise is
    // handed straight to ClipboardItem so the whole fonts/decode/capture
    // chain runs inside it, keeping clipboard.write() itself synchronous
    // with this click (OV-2 / Safari-iOS gesture-chain requirement).
    const blobPromise = captureNodeToBlob(node, { scale });
    navigator.clipboard
      .write([new ClipboardItem({ "image/png": blobPromise })])
      .then(() => setCopyStatus("done"))
      .catch(async () => {
        // Genuine denial or a browser that rejects a pending-promise
        // ClipboardItem — fall back to download rather than leaving the
        // user with no result.
        try {
          await handleDownload();
          setMessage("Clipboard access denied — downloaded instead.");
        } finally {
          setCopyStatus("error");
        }
      });
  }

  async function handleCopyLink() {
    setLinkStatus("busy");
    try {
      await navigator.clipboard.writeText(shareUrl);
      setLinkStatus("done");
    } catch (err) {
      setLinkStatus("error");
      setMessage((err as Error).message);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      <div style={{ display: "flex", gap: 8 }}>
        <button type="button" onClick={handleDownload} disabled={disabled || downloadStatus === "busy"}>
          {downloadStatus === "busy" ? "Exporting…" : "Download PNG"}
        </button>
        <button type="button" onClick={handleCopy} disabled={disabled || copyStatus === "busy"}>
          {copyStatus === "busy" ? "Copying…" : "Copy image"}
        </button>
        <button type="button" onClick={handleCopyLink} disabled={disabled || linkStatus === "busy"}>
          {linkStatus === "done" ? "Link copied" : "Copy shareable link"}
        </button>
      </div>
      {message && <p role="status">{message}</p>}
    </div>
  );
}
