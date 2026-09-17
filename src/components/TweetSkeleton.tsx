// Tweet-shaped loading skeleton (Section 4C) — distinguishes "loading" from
// "frozen" on a slow connection, and previews the real card's layout.
export function TweetSkeleton() {
  return (
    <div
      aria-busy="true"
      aria-label="Loading tweet"
      style={{
        width: 500,
        maxWidth: "100%",
        border: "1px solid #eee",
        borderRadius: 16,
        padding: 16,
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
        <div style={{ width: 40, height: 40, borderRadius: "50%", background: "#e8e8e8" }} />
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <div style={{ width: 120, height: 12, borderRadius: 4, background: "#e8e8e8" }} />
          <div style={{ width: 80, height: 10, borderRadius: 4, background: "#eee" }} />
        </div>
      </div>
      <div style={{ width: "100%", height: 12, borderRadius: 4, background: "#eee" }} />
      <div style={{ width: "70%", height: 12, borderRadius: 4, background: "#eee" }} />
    </div>
  );
}
