import type { Position } from "../types/models";
import { money, pct } from "../lib/utils";
import { Card } from "./ui/Card";

export function PositionsTable({ positions }: { positions: Position[] }) {
  return (
    <Card className="overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-900/60 text-slate-400">
            <tr>
              {["Ticker", "State", "Entry Date", "Entry Price", "Current Close", "Unrealized PnL", "Probability", "Bands", "Message"].map((head) => (
                <th key={head} className="px-4 py-3 font-medium">
                  {head}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {positions.map((position) => (
              <tr key={position.ticker} className="border-t border-slate-800 text-slate-200">
                <td className="px-4 py-4 font-semibold">{position.ticker}</td>
                <td className="px-4 py-4">{position.state}</td>
                <td className="px-4 py-4">{position.entry_date ?? "N/A"}</td>
                <td className="px-4 py-4">
                  {position.entry_display_price ? money(position.entry_display_price) : position.entry_price ? money(position.entry_price) : "N/A"}
                </td>
                <td className="px-4 py-4">{money(position.current_close)}</td>
                <td className={`px-4 py-4 ${position.unrealized_pnl_pct >= 0 ? "text-emerald-300" : "text-red-300"}`}>
                  {pct(position.unrealized_pnl_pct / 100, 2)}
                </td>
                <td className="px-4 py-4">{pct(position.probability, 1)}</td>
                <td className="px-4 py-4">
                  Entry {pct(position.entry_band, 0)} / Exit {pct(position.exit_band, 0)}
                </td>
                <td className="px-4 py-4 max-w-md text-slate-300">{position.latest_message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
