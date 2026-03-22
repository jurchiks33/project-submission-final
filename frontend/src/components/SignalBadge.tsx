import type { ActionType } from "../types/models";
import { cn } from "../lib/utils";

const styles: Record<ActionType, string> = {
  "Enter Next Opening": "bg-emerald-500/20 text-emerald-300",
  "Exit Next Opening": "bg-orange-500/20 text-orange-300",
  "Hold Long Position": "bg-sky-500/20 text-sky-300",
  Flat: "bg-slate-700 text-slate-300",
  "Awaiting Next Open Fill": "bg-amber-500/20 text-amber-300",
};

export function SignalBadge({ action }: { action: ActionType }) {
  return <span className={cn("rounded-full px-3 py-1 text-xs font-medium", styles[action])}>{action}</span>;
}
