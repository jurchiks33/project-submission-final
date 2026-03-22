import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { PositionsTable } from "../components/PositionsTable";
import { usePositions } from "../hooks/usePositions";
import { useQueryClient } from "@tanstack/react-query";

export function PositionsPage() {
  const { data, isLoading } = usePositions();
  const queryClient = useQueryClient();

  if (isLoading || !data) {
    return <div className="text-slate-400">Loading positions...</div>;
  }

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-slate-50">Ledger and active positions</h2>
            <p className="mt-1 text-sm text-slate-400">
              View open positions, queued actions, and current after-close state.
            </p>
          </div>
          <Button variant="secondary" onClick={() => queryClient.invalidateQueries({ queryKey: ["positions"] })}>
            Reload ledger
          </Button>
        </div>
      </Card>

      <PositionsTable positions={data} />
    </div>
  );
}
