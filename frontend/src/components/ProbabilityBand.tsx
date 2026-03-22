import { pct } from "../lib/utils";

interface Props {
  probability: number;
  entry: number;
  exit: number;
}

export function ProbabilityBand({ probability, entry, exit }: Props) {
  const position = Math.min(100, Math.max(0, probability * 100));
  return (
    <div className="min-w-[170px]">
      <div className="mb-1 flex items-center justify-between text-xs text-slate-400">
        <span>Prob {pct(probability, 0)}</span>
        <span>Entry {pct(entry, 0)} / Exit {pct(exit, 0)}</span>
      </div>
      <div className="relative h-2 rounded-full bg-slate-800">
        <div className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-slate-600 via-sky-500 to-emerald-400" style={{ width: `${position}%` }} />
        <div className="absolute inset-y-[-4px] w-px bg-amber-300" style={{ left: `${entry * 100}%` }} />
        <div className="absolute inset-y-[-4px] w-px bg-rose-300" style={{ left: `${exit * 100}%` }} />
      </div>
    </div>
  );
}
