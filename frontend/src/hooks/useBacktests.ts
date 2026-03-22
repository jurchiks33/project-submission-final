import { useQuery } from "@tanstack/react-query";
import { fetchBacktestSummary, fetchTickerBacktest } from "../api";

export function useBacktestSummary() {
  return useQuery({
    queryKey: ["backtest-summary"],
    queryFn: fetchBacktestSummary,
  });
}

export function useTickerBacktest(ticker: string) {
  return useQuery({
    queryKey: ["backtest-detail", ticker],
    queryFn: () => fetchTickerBacktest(ticker),
    enabled: Boolean(ticker),
  });
}
