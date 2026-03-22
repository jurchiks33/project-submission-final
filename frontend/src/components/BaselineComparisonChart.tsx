import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { BacktestDetail } from "../types/models";
import { Card } from "./ui/Card";

export function BaselineComparisonChart({ detail }: { detail: BacktestDetail }) {
  const baseline = detail.baseline_metrics;
  const data = [
    {
      metric: "Return %",
      strategy: detail.metrics.total_return_pct,
      baseline: baseline?.total_return_pct ?? 0,
    },
    {
      metric: "Drawdown %",
      strategy: detail.metrics.max_drawdown_pct,
      baseline: baseline?.max_drawdown_pct ?? 0,
    },
    {
      metric: "Volatility %",
      strategy: detail.metrics.volatility_pct,
      baseline: baseline?.volatility_pct ?? 0,
    },
  ];
  return (
    <Card>
      <h3 className="mb-4 text-lg font-semibold text-slate-50">Strategy vs baseline</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid stroke="#243042" strokeDasharray="3 3" />
            <XAxis dataKey="metric" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <Bar dataKey="strategy" fill="#4fd1c5" radius={[6, 6, 0, 0]} />
            <Bar dataKey="baseline" fill="#64748b" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
