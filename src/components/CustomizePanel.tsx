import { BACKGROUND_PRESETS, Scale, StyleState } from "@/lib/style-state";

export interface CustomizePanelProps {
  style: StyleState;
  onChange: (next: StyleState) => void;
}

/**
 * Owns theme/background/padding/scale controls. Does not own the tweet
 * data, export logic, or URL persistence (eng review Section C).
 */
export function CustomizePanel({ style, onChange }: CustomizePanelProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, minWidth: 220 }}>
      <fieldset>
        <legend>Background</legend>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {BACKGROUND_PRESETS.map((preset) => (
            <button
              key={preset.id}
              type="button"
              aria-pressed={style.backgroundId === preset.id}
              aria-label={preset.label}
              onClick={() => onChange({ ...style, backgroundId: preset.id })}
              style={{
                width: 32,
                height: 32,
                borderRadius: 6,
                background: preset.css,
                border: style.backgroundId === preset.id ? "2px solid #1d9bf0" : "1px solid #ccc",
                cursor: "pointer",
              }}
            />
          ))}
        </div>
      </fieldset>

      <label style={{ display: "flex", flexDirection: "column", gap: 4 }}>
        Padding: {style.padding}px
        <input
          type="range"
          min={0}
          max={120}
          value={style.padding}
          onChange={(e) => onChange({ ...style, padding: Number(e.target.value) })}
          aria-label="Padding"
        />
      </label>

      <fieldset>
        <legend>Export scale</legend>
        <div role="radiogroup" aria-label="Export scale" style={{ display: "flex", gap: 8 }}>
          {([1, 2, 3] as Scale[]).map((scale) => (
            <button
              key={scale}
              type="button"
              role="radio"
              aria-checked={style.scale === scale}
              onClick={() => onChange({ ...style, scale })}
              style={{
                padding: "4px 10px",
                fontWeight: style.scale === scale ? "bold" : "normal",
              }}
            >
              {scale}x
            </button>
          ))}
        </div>
      </fieldset>

      <fieldset>
        <legend>Theme</legend>
        <div role="radiogroup" aria-label="Theme" style={{ display: "flex", gap: 8 }}>
          {(["light", "dark"] as const).map((theme) => (
            <button
              key={theme}
              type="button"
              role="radio"
              aria-checked={style.theme === theme}
              onClick={() => onChange({ ...style, theme })}
              style={{
                padding: "4px 10px",
                fontWeight: style.theme === theme ? "bold" : "normal",
              }}
            >
              {theme}
            </button>
          ))}
        </div>
      </fieldset>
    </div>
  );
}
