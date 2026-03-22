import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { ExplanationPanel } from "../components/ExplanationPanel";
import { GateBadge } from "../components/GateBadge";
import { MetricCard } from "../components/MetricCard";
import { SignalBadge } from "../components/SignalBadge";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { useSignalDetail } from "../hooks/useSignals";
import { useRunTicker } from "../hooks/usePipelineActions";
import { money, pct } from "../lib/utils";

export function TickerDetailPage() {
  const { ticker = "" } = useParams();
  const detailQuery = useSignalDetail(ticker);
  const runTicker = useRunTicker();

  const detail = useMemo(() => detailQuery.data, [detailQuery.data]);
  if (detailQuery.isLoading || !detail) {
    return <div className="text-slate-400">Loading ticker detail...</div>;
  }

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-accent/80">Ticker detail</p>
            <h2 className="mt-2 text-3xl font-semibold text-slate-50">{detail.ticker}</h2>
            <div className="mt-4 flex flex-wrap gap-3">
              <SignalBadge action={detail.action} />
              <GateBadge label="Trend gate" passed={detail.trend_gate} />
              <GateBadge label="Vol gate" passed={detail.vol_gate} />
              <GateBadge label="Quality gate" passed={detail.quality_gate} />
            </div>
          </div>
          <Button
            onClick={() => runTicker.mutate(detail.ticker)}
            disabled={runTicker.isPending}
          >
            {runTicker.isPending ? "Running ticker..." : "Run Single Ticker"}
          </Button>
        </div>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Current state" value={detail.current_state} />
        <MetricCard label="Last close" value={money(detail.last_close)} />
        <MetricCard label="Probability" value={pct(detail.probability, 1)} />
        <MetricCard label="Entry / Exit" value={`${pct(detail.entry_band, 0)} / ${pct(detail.exit_band, 0)}`} />
      </div>

      <Card>
        <h3 className="text-lg font-semibold text-slate-50">Signal state and risk</h3>
        <div className="mt-4 grid gap-6 lg:grid-cols-2">
          <div>
            <p className="text-sm text-slate-400">Pending action</p>
            <p className="mt-1 text-slate-100">{detail.pending_action ?? "None"}</p>
            <p className="mt-4 text-sm text-slate-400">Latest message</p>
            <p className="mt-1 text-slate-100">{detail.latest_message}</p>
          </div>
          <div>
            <p className="text-sm text-slate-400">State transitions</p>
            <ul className="mt-2 space-y-2 text-sm text-slate-200">
              {detail.state_transitions.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
            <p className="mt-4 text-sm text-slate-400">Risk notes</p>
            <ul className="mt-2 space-y-2 text-sm text-slate-200">
              {detail.risk_notes.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </Card>

      <ExplanationPanel explanation={detail.explanation} />
    </div>
  );
}
