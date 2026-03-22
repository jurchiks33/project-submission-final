import { Card } from "./ui/Card";

interface Props {
  label: string;
  value: string | number;
}

export function MetricCard({ label, value }: Props) {
  return (
    <Card className="bg-panelAlt p-4">
      <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-2 text-xl font-semibold text-slate-50">{value}</p>
    </Card>
  );
}
