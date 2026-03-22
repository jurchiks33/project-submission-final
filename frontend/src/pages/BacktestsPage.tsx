import { useEffect, useMemo, useState } from "react";
import { BaselineComparisonChart } from "../components/BaselineComparisonChart";
import { EquityCurveChart } from "../components/EquityCurveChart";
import { MetricCard } from "../components/MetricCard";
import { Card } from "../components/ui/Card";
import { useBacktestSummary, useTickerBacktest } from "../hooks/useBacktests";
import { useSignals } from "../hooks/useSignals";
import { money, pct } from "../lib/utils";

export function BacktestsPage() {
  const { data: signals } = useSignals();
  const tickers = useMemo(() => {
    const items = signals?.map((item) => item.ticker) ?? [];
    return items.length ? items : ["MSFT"];
  }, [signals]);
  const [selectedTicker, setSelectedTicker] = useState("MSFT");
  const summaryQuery = useBacktestSummary();
  const detailQuery = useTickerBacktest(selectedTicker);

  useEffect(() => {
    if (!tickers.includes(selectedTicker) && tickers.length) {
      setSelectedTicker(tickers[0]);
    }
  }, [selectedTicker, tickers]);

  const summary = useMemo(() => summaryQuery.data, [summaryQuery.data]);
  const detail = useMemo(() => detailQuery.data, [detailQuery.data]);

  if (summaryQuery.isLoading || detailQuery.isLoading || !summary || !detail) {
    return <div className="text-slate-400">Loading backtests...</div>;
  }

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-slate-50">Backtest summary</h2>
            <p className="mt-1 text-sm text-slate-400">Portfolio-level summary plus per-ticker inspection.</p>
          </div>
          <select
            className="rounded-xl border border-border bg-panelAlt px-4 py-3 text-sm text-slate-100"
            value={selectedTicker}
            onChange={(event) => setSelectedTicker(event.target.value)}
          >
            {tickers.map((ticker) => (
              <option key={ticker} value={ticker}>
                {ticker}
              </option>
            ))}
          </select>
        </div>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <MetricCard label="Total start value" value={money(summary.total_start_value)} />
        <MetricCard label="Total end value" value={money(summary.total_end_value)} />
        <MetricCard label="Total PnL" value={money(summary.total_pnl)} />
        <MetricCard label="Total return" value={pct(summary.total_return_pct / 100, 2)} />
        <MetricCard label="Tickers processed" value={summary.tickers_processed} />
        <MetricCard label="Beat baseline count" value={summary.beat_baseline_count} />
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Strategy return" value={pct(detail.metrics.total_return_pct / 100, 2)} />
        <MetricCard label="Max drawdown" value={pct(detail.metrics.max_drawdown_pct / 100, 2)} />
        <MetricCard label="Volatility" value={pct(detail.metrics.volatility_pct / 100, 2)} />
        <MetricCard label="Total trades" value={detail.metrics.total_trades} />
        <MetricCard label="Win rate" value={pct(detail.metrics.win_rate_pct / 100, 2)} />
        <MetricCard label="Profit factor" value={detail.metrics.profit_factor.toFixed(2)} />
        <MetricCard label="Expectancy" value={money(detail.metrics.expectancy)} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <EquityCurveChart data={detail.equity_curve} />
        <BaselineComparisonChart detail={detail} />
      </div>
    </div>
  );
}
