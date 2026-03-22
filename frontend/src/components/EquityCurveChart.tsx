import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { EquityPoint } from "../types/models";
import { Card } from "./ui/Card";

export function EquityCurveChart({ data }: { data: EquityPoint[] }) {
  return (
    <Card>
      <h3 className="mb-4 text-lg font-semibold text-slate-50">Equity curve</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="#243042" strokeDasharray="3 3" />
            <XAxis dataKey="date" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="strategy" stroke="#4fd1c5" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="baseline" stroke="#64748b" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
