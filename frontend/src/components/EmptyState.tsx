import { Card } from "./ui/Card";

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <Card className="border-dashed border-slate-700 text-center">
      <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
      <p className="mt-2 text-sm text-slate-400">{description}</p>
    </Card>
  );
}
