import { useSignals } from "../hooks/useSignals";
import { SignalBadge } from "../components/SignalBadge";
import { Card } from "../components/ui/Card";
import { GateBadge } from "../components/GateBadge";
import { pct } from "../lib/utils";

export function SignalsLogPage() {
  const { data, isLoading } = useSignals();

  if (isLoading || !data) {
    return <div className="text-slate-400">Loading signals log...</div>;
  }

  return (
    <div className="space-y-4">
      <Card>
        <h2 className="text-2xl font-semibold text-slate-50">Signals log</h2>
        <p className="mt-1 text-sm text-slate-400">
          Chronological view of after-close outputs with probability and rule context.
        </p>
      </Card>
      {data.map((signal) => (
        <Card key={signal.ticker} className="bg-panelAlt">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-3">
                <h3 className="text-xl font-semibold text-slate-50">{signal.ticker}</h3>
                <SignalBadge action={signal.action} />
                <span className="text-xs text-slate-500">{signal.signal_date}</span>
              </div>
              <p className="mt-3 text-sm text-slate-300">{signal.latest_message}</p>
              <p className="mt-2 text-sm text-slate-400">{signal.short_explanation}</p>
            </div>
            <div className="text-sm text-slate-300">
              <p>Probability: {pct(signal.probability, 1)}</p>
              <p className="mt-1">State: {signal.current_state}</p>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <GateBadge label="Trend gate" passed={signal.trend_gate} />
            <GateBadge label="Vol gate" passed={signal.vol_gate} />
            <GateBadge label="Quality gate" passed={signal.quality_gate} />
          </div>
        </Card>
      ))}
    </div>
  );
}
