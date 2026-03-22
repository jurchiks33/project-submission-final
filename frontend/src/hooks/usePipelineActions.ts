import { useMutation, useQueryClient } from "@tanstack/react-query";
import { runTickerPipeline, runUniversePipeline } from "../api";

const invalidateKeys = [
  ["dashboard"],
  ["pipeline-status"],
  ["signals"],
  ["positions"],
  ["backtest-summary"],
];

export function useRunUniverse() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: runUniversePipeline,
    onSuccess: async () => {
      await Promise.all(invalidateKeys.map((key) => queryClient.invalidateQueries({ queryKey: key })));
    },
  });
}

export function useRunTicker() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: runTickerPipeline,
    onSuccess: async (_, ticker) => {
      await Promise.all([
        ...invalidateKeys.map((key) => queryClient.invalidateQueries({ queryKey: key })),
        queryClient.invalidateQueries({ queryKey: ["signal-detail", ticker] }),
        queryClient.invalidateQueries({ queryKey: ["backtest-detail", ticker] }),
      ]);
    },
  });
}
