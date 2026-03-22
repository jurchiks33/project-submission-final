import { apiClient } from "./client";
import type {
  BacktestDetail,
  BacktestSummary,
  DashboardPayload,
  PipelineRunResponse,
  PipelineStatus,
  Position,
  RuntimeSettings,
  SignalRow,
  TickerDetail,
} from "../types/models";

export async function fetchDashboard() {
  const { data } = await apiClient.get<DashboardPayload>("/dashboard");
  return data;
}

export async function fetchPipelineStatus() {
  const { data } = await apiClient.get<PipelineStatus>("/pipeline/status");
  return data;
}

export async function runUniversePipeline() {
  const { data } = await apiClient.post<PipelineRunResponse>("/pipeline/run-universe");
  return data;
}

export async function runTickerPipeline(ticker: string) {
  const { data } = await apiClient.post<PipelineRunResponse>(`/pipeline/run-ticker/${ticker}`);
  return data;
}

export async function fetchSignals() {
  const { data } = await apiClient.get<SignalRow[]>("/signals");
  return data;
}

export async function fetchSignalDetail(ticker: string) {
  const { data } = await apiClient.get<TickerDetail>(`/signals/${ticker}`);
  return data;
}

export async function fetchPositions() {
  const { data } = await apiClient.get<Position[]>("/positions");
  return data;
}

export async function fetchBacktestSummary() {
  const { data } = await apiClient.get<BacktestSummary>("/backtests/summary");
  return data;
}

export async function fetchTickerBacktest(ticker: string) {
  const { data } = await apiClient.get<BacktestDetail>(`/backtests/${ticker}`);
  return data;
}

export async function fetchSettings() {
  const { data } = await apiClient.get<RuntimeSettings>("/settings");
  return data;
}
