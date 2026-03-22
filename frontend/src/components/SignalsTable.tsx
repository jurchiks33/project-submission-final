import { Link } from "react-router-dom";
import type { SignalRow } from "../types/models";
import { money, num } from "../lib/utils";
import { GateBadge } from "./GateBadge";
import { ProbabilityBand } from "./ProbabilityBand";
import { SignalBadge } from "./SignalBadge";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";

export function SignalsTable({ signals }: { signals: SignalRow[] }) {
  return (
    <Card className="overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-900/60 text-slate-400">
            <tr>
              {["Ticker", "Action", "Probability", "Gates", "State", "Last Close", "Explanation", "Details"].map((head) => (
                <th key={head} className="px-4 py-3 font-medium">
                  {head}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {signals.map((signal) => (
              <tr key={signal.ticker} className="border-t border-slate-800 text-slate-200">
                <td className="px-4 py-4">
                  <div className="font-semibold">{signal.ticker}</div>
                  <div className="text-xs text-slate-500">{signal.signal_date}</div>
                </td>
                <td className="px-4 py-4">
                  <SignalBadge action={signal.action} />
                </td>
                <td className="px-4 py-4">
                  <ProbabilityBand probability={signal.probability} entry={signal.entry_band} exit={signal.exit_band} />
                </td>
                <td className="px-4 py-4">
                  <div className="flex flex-wrap gap-2">
                    <GateBadge label="Trend" passed={signal.trend_gate} />
                    <GateBadge label="Vol" passed={signal.vol_gate} />
                    <GateBadge label="Quality" passed={signal.quality_gate} />
                  </div>
                </td>
                <td className="px-4 py-4">
                  <div>{signal.current_state}</div>
                  <div className="text-xs text-slate-500">{signal.pending_action ?? "No pending state change"}</div>
                </td>
                <td className="px-4 py-4">
                  <div>{money(signal.last_close)}</div>
                  <div className="text-xs text-slate-500">Rank {signal.rank ?? "-"}</div>
                </td>
                <td className="px-4 py-4">
                  <div className="max-w-sm">{signal.short_explanation}</div>
                  <div className="mt-1 text-xs text-slate-500">{signal.latest_message}</div>
                </td>
                <td className="px-4 py-4">
                  <Link to={`/ticker/${signal.ticker}`}>
                    <Button variant="secondary">Inspect</Button>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {!signals.length ? <div className="p-6 text-sm text-slate-400">No signals available.</div> : null}
    </Card>
  );
}
