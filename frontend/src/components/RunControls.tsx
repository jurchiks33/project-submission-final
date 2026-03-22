import { useState } from "react";
import { Button } from "./ui/Button";
import { Card } from "./ui/Card";

interface Props {
  onRunUniverse: () => Promise<void>;
  onRefresh: () => Promise<void>;
  runningUniverse?: boolean;
  refreshing?: boolean;
}

export function RunControls({ onRunUniverse, onRefresh, runningUniverse, refreshing }: Props) {
  const [error, setError] = useState<string | null>(null);

  async function handle(action: () => Promise<void>) {
    try {
      setError(null);
      await action();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    }
  }

  return (
    <Card>
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-50">Run controls</h2>
          <p className="mt-1 text-sm text-slate-400">
            Trigger the daily after-close workflow, refresh outputs, and keep dashboard state in sync.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button onClick={() => handle(onRunUniverse)} disabled={runningUniverse}>
            {runningUniverse ? "Running universe..." : "Run Universe"}
          </Button>
          <Button variant="secondary" onClick={() => handle(onRefresh)} disabled={refreshing}>
            {refreshing ? "Refreshing..." : "Refresh Outputs"}
          </Button>
        </div>
      </div>
      {error ? <p className="mt-4 text-sm text-red-300">{error}</p> : null}
    </Card>
  );
}
