import { useQuery } from "@tanstack/react-query";
import { fetchSignalDetail, fetchSignals } from "../api";

export function useSignals() {
  return useQuery({
    queryKey: ["signals"],
    queryFn: fetchSignals,
  });
}

export function useSignalDetail(ticker: string) {
  return useQuery({
    queryKey: ["signal-detail", ticker],
    queryFn: () => fetchSignalDetail(ticker),
    enabled: Boolean(ticker),
  });
}
