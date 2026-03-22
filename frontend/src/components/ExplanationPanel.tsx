import type { ExplanationPayload } from "../types/models";
import { pct } from "../lib/utils";
import { DriverImpactList } from "./DriverImpactList";
import { GateBadge } from "./GateBadge";
import { Card } from "./ui/Card";

export function ExplanationPanel({ explanation }: { explanation: ExplanationPayload }) {
  const grouped = ["momentum", "trend", "volatility", "market"] as const;
  return (
    <Card>
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-accent/80">Decision explanation</p>
          <h3 className="mt-2 text-xl font-semibold text-slate-50">{explanation.final_action}</h3>
          <p className="mt-3 max-w-3xl text-sm text-slate-300">{explanation.plain_summary}</p>
        </div>
        <div className="rounded-2xl border border-border bg-panelAlt px-4 py-3 text-right">
          <p className="text-xs text-slate-500">Model output</p>
          <p className="text-2xl font-semibold text-slate-50">{pct(explanation.model_probability, 1)}</p>
          <p className="text-xs text-slate-500">{explanation.decision_type}</p>
        </div>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-3">
        <GateBadge label="Trend gate" passed={explanation.gate_reasoning.trend_gate} />
        <GateBadge label="Volatility gate" passed={explanation.gate_reasoning.vol_gate} />
        <GateBadge label="Quality gate" passed={explanation.gate_reasoning.quality_gate} />
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <Card className="bg-panelAlt">
          <p className="text-sm font-semibold text-slate-100">Confidence and rationale</p>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            <li>Model output: probability scored at {pct(explanation.model_probability, 1)}.</li>
            <li>Rules and gates: technical filters were applied after the model output.</li>
            <li>Final action: the state machine translated model plus rules into the after-close instruction.</li>
          </ul>
        </Card>
        <Card className="bg-panelAlt">
          <p className="text-sm font-semibold text-slate-100">Gate reasoning notes</p>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            {explanation.gate_reasoning.notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        </Card>
      </div>

      <div className="mt-6 space-y-4">
        {grouped.map((category) => {
          const drivers = explanation.key_drivers.filter((item) => item.category === category);
          if (!drivers.length) return null;
          return (
            <div key={category}>
              <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-slate-400">{category}</p>
              <DriverImpactList drivers={drivers} />
            </div>
          );
        })}
      </div>

      <Card className="mt-6 border-dashed border-slate-700 bg-transparent">
        <p className="text-sm font-medium text-slate-200">Future feature contribution chart</p>
        <p className="mt-2 text-sm text-slate-400">
          Reserved area for a future SHAP-style bar chart or per-feature attribution view once the Python engine exposes that data.
        </p>
      </Card>
    </Card>
  );
}
