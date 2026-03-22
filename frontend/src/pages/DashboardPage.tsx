import { useMemo, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { PipelineStatusCard } from "../components/PipelineStatusCard";
import { RunControls } from "../components/RunControls";
import { SignalsTable } from "../components/SignalsTable";
import { SummaryCard } from "../components/SummaryCard";
import { Card } from "../components/ui/Card";
import { useDashboard } from "../hooks/useDashboard";
import { useRunUniverse } from "../hooks/usePipelineActions";
import { pct } from "../lib/utils";

export function DashboardPage() {
  const { data, isLoading, refetch } = useDashboard();
  const runUniverse = useRunUniverse();
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [actionFilter, setActionFilter] = useState("all");
  const [stateFilter, setStateFilter] = useState("all");
  const [gateFilter, setGateFilter] = useState("all");

  const signals = useMemo(() => {
    const source = data?.signals ?? [];
    return source.filter((signal) => {
      const matchesSearch = signal.ticker.toLowerCase().includes(search.toLowerCase());
      const matchesAction = actionFilter === "all" || signal.action === actionFilter;
      const matchesState = stateFilter === "all" || signal.current_state === stateFilter;
      const matchesGate =
        gateFilter === "all" ||
        (gateFilter === "blocked" ? signal.gate_blocked : !signal.gate_blocked);
      return matchesSearch && matchesAction && matchesState && matchesGate;
    });
  }, [actionFilter, data?.signals, gateFilter, search, stateFilter]);

  async function refreshAll() {
    await Promise.all([
      refetch(),
      queryClient.invalidateQueries({ queryKey: ["signals"] }),
      queryClient.invalidateQueries({ queryKey: ["positions"] }),
      queryClient.invalidateQueries({ queryKey: ["backtest-summary"] }),
      queryClient.invalidateQueries({ queryKey: ["pipeline-status"] }),
    ]);
  }

  if (isLoading || !data) {
    return <div className="text-slate-400">Loading dashboard...</div>;
  }

  return (
    <div className="space-y-6">
      <RunControls
        onRunUniverse={async () => {
          await runUniverse.mutateAsync();
        }}
        onRefresh={refreshAll}
        runningUniverse={runUniverse.isPending}
      />

      <div className="grid gap-4 xl:grid-cols-[1.4fr_1fr]">
        <PipelineStatusCard status={data.status} />
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <SummaryCard label="Active long positions" value={data.summary.active_long_positions} />
          <SummaryCard label="New entries" value={data.summary.new_entries} />
          <SummaryCard label="New exits" value={data.summary.new_exits} />
          <SummaryCard label="Blocked signals" value={data.summary.blocked_signals} />
          <SummaryCard label="Aggregate return" value={pct(data.summary.aggregate_return / 100, 2)} />
          <SummaryCard label="Beat baseline count" value={data.summary.baseline_comparison_count} />
        </div>
      </div>

      <Card>
        <div className="flex flex-col gap-4 lg:flex-row">
          <input
            className="rounded-xl border border-border bg-panelAlt px-4 py-3 text-sm text-slate-100 outline-none"
            placeholder="Search ticker"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
          <select
            className="rounded-xl border border-border bg-panelAlt px-4 py-3 text-sm text-slate-100"
            value={actionFilter}
            onChange={(event) => setActionFilter(event.target.value)}
          >
            <option value="all">All actions</option>
            <option value="Enter Next Opening">Enter Next Opening</option>
            <option value="Exit Next Opening">Exit Next Opening</option>
            <option value="Hold Long Position">Hold Long Position</option>
            <option value="Flat">Flat</option>
          </select>
          <select
            className="rounded-xl border border-border bg-panelAlt px-4 py-3 text-sm text-slate-100"
            value={stateFilter}
            onChange={(event) => setStateFilter(event.target.value)}
          >
            <option value="all">All states</option>
            <option value="Long">Long</option>
            <option value="Flat">Flat</option>
            <option value="Awaiting Next Open Fill">Awaiting Next Open Fill</option>
          </select>
          <select
            className="rounded-xl border border-border bg-panelAlt px-4 py-3 text-sm text-slate-100"
            value={gateFilter}
            onChange={(event) => setGateFilter(event.target.value)}
          >
            <option value="all">All gate outcomes</option>
            <option value="blocked">Blocked</option>
            <option value="passed">Passed</option>
          </select>
        </div>
      </Card>

      <SignalsTable signals={signals} />
    </div>
  );
}
