import { Card } from "./ui/Card";

interface SummaryCardProps {
  label: string;
  value: string | number;
  note?: string;
}

export function SummaryCard({ label, value, note }: SummaryCardProps) {
  return (
    <Card className="bg-panelAlt">
      <p className="text-sm text-slate-400">{label}</p>
      <div className="mt-3 text-3xl font-semibold text-slate-50">{value}</div>
      {note ? <p className="mt-2 text-xs text-slate-500">{note}</p> : null}
    </Card>
  );
}
