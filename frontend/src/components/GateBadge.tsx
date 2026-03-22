import { cn } from "../lib/utils";

interface Props {
  label: string;
  passed: boolean | null;
}

export function GateBadge({ label, passed }: Props) {
  const text = passed === null ? "N/A" : passed ? "Pass" : "Block";
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs",
        passed === null
          ? "bg-slate-700 text-slate-300"
          : passed
            ? "bg-emerald-500/15 text-emerald-300"
            : "bg-red-500/15 text-red-300",
      )}
    >
      <span>{label}</span>
      <span>{text}</span>
    </span>
  );
}
