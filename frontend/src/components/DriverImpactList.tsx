import type { KeyDriver } from "../types/models";
import { Card } from "./ui/Card";

export function DriverImpactList({ drivers }: { drivers: KeyDriver[] }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {drivers.map((driver) => (
        <Card key={`${driver.feature}-${driver.category}`} className="bg-panelAlt p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-100">{driver.feature}</p>
              <p className="text-xs uppercase tracking-wide text-slate-500">{driver.category}</p>
            </div>
            <span className={driver.direction === "up" ? "text-emerald-300" : "text-red-300"}>
              {driver.direction === "up" ? "Pushed up" : "Pushed down"}
            </span>
          </div>
          <p className="mt-3 text-sm text-slate-300">{driver.human_reason}</p>
          <p className="mt-2 text-xs text-slate-500">Impact strength: {driver.impact.toFixed(2)}</p>
        </Card>
      ))}
    </div>
  );
}
