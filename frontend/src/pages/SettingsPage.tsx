import { Card } from "../components/ui/Card";
import { useSettings } from "../hooks/useSettings";

export function SettingsPage() {
  const { data, isLoading } = useSettings();

  if (isLoading || !data) {
    return <div className="text-slate-400">Loading settings...</div>;
  }

  const fields = Object.entries(data);

  return (
    <div className="space-y-6">
      <Card>
        <h2 className="text-2xl font-semibold text-slate-50">Runtime settings</h2>
        <p className="mt-1 text-sm text-slate-400">
          Read-only configuration now, structured so save/edit actions can be added later.
        </p>
      </Card>
      <div className="grid gap-4 md:grid-cols-2">
        {fields.map(([key, value]) => (
          <Card key={key} className="bg-panelAlt">
            <p className="text-xs uppercase tracking-wide text-slate-500">{key}</p>
            <p className="mt-2 text-lg font-medium text-slate-50">{String(value)}</p>
          </Card>
        ))}
      </div>
      <Card className="border-dashed border-slate-700">
        <p className="text-sm font-medium text-slate-200">Save later structure</p>
        <p className="mt-2 text-sm text-slate-400">
          This page is read-only today. The backend and form layout are ready for a future save endpoint once you decide to edit settings from the UI.
        </p>
      </Card>
    </div>
  );
}
