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
  const segBtn = (active: boolean) =>
    `flex-1 rounded-md border px-2 py-1.5 text-xs font-medium ${
      active
        ? "border-accent bg-accent/10 text-accent"
        : "border-border bg-transparent text-foreground hover:bg-zinc-50"
    }`;

  return (
    <div className="flex min-w-[220px] flex-col gap-5.5">
      <fieldset>
        <legend className="mb-2.5 text-xs font-semibold uppercase tracking-wide text-text-secondary">
          Background
        </legend>
        <div className="flex flex-wrap gap-2">
          {BACKGROUND_PRESETS.map((preset) => (
            <button
              key={preset.id}
              type="button"
              aria-pressed={style.backgroundId === preset.id}
              aria-label={preset.label}
              onClick={() => onChange({ ...style, backgroundId: preset.id })}
              className={`h-7 w-7 cursor-pointer rounded-lg ${
                style.backgroundId === preset.id ? "ring-2 ring-accent ring-offset-2" : "border border-border"
              }`}
              style={{ background: preset.css }}
            />
          ))}
        </div>
      </fieldset>

      <label className="flex flex-col gap-2.5">
        <span className="text-xs font-semibold uppercase tracking-wide text-text-secondary">
          Padding — {style.padding}px
        </span>
        <input
          type="range"
          min={0}
          max={120}
          value={style.padding}
          onChange={(e) => onChange({ ...style, padding: Number(e.target.value) })}
          aria-label="Padding"
          className="w-full accent-accent"
        />
      </label>

      <fieldset>
        <legend className="mb-2.5 text-xs font-semibold uppercase tracking-wide text-text-secondary">
          Export scale
        </legend>
        <div role="radiogroup" aria-label="Export scale" className="flex gap-1.5">
          {([1, 2, 3] as Scale[]).map((scale) => (
            <button
              key={scale}
              type="button"
              role="radio"
              aria-checked={style.scale === scale}
              onClick={() => onChange({ ...style, scale })}
              className={segBtn(style.scale === scale)}
            >
              {scale}x
            </button>
          ))}
        </div>
      </fieldset>

      <fieldset>
        <legend className="mb-2.5 text-xs font-semibold uppercase tracking-wide text-text-secondary">
          Theme
        </legend>
        <div role="radiogroup" aria-label="Theme" className="flex gap-1.5">
          {(["light", "dark"] as const).map((theme) => (
            <button
              key={theme}
              type="button"
              role="radio"
              aria-checked={style.theme === theme}
              onClick={() => onChange({ ...style, theme })}
              className={`${segBtn(style.theme === theme)} capitalize`}
            >
              {theme}
            </button>
          ))}
        </div>
      </fieldset>
    </div>
  );
}
