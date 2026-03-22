import type { PipelineStatus } from "../types/models";
import { fmtDate } from "../lib/utils";
import { Card } from "./ui/Card";

interface Props {
  status: PipelineStatus;
}

export function PipelineStatusCard({ status }: Props) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-50">Pipeline status</h2>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs uppercase tracking-wide text-accent">
          {status.status}
        </span>
      </div>
      <div className="mt-4 grid gap-3 text-sm text-slate-300 md:grid-cols-2">
        <div>
          <p className="text-slate-500">Latest run time</p>
          <p>{fmtDate(status.latest_run_time)}</p>
        </div>
        <div>
          <p className="text-slate-500">Latest signal date</p>
          <p>{status.latest_signal_date ?? "N/A"}</p>
        </div>
        <div>
          <p className="text-slate-500">Tickers processed</p>
          <p>{status.tickers_processed}</p>
        </div>
        <div>
          <p className="text-slate-500">Last run mode</p>
          <p>{status.last_run_mode ?? "N/A"}</p>
        </div>
      </div>
      {status.last_error ? <p className="mt-4 text-sm text-red-300">{status.last_error}</p> : null}
    </Card>
  );
}
