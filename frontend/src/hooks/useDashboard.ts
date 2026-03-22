import { useQuery } from "@tanstack/react-query";
import { fetchDashboard, fetchPipelineStatus } from "../api";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: fetchDashboard,
  });
}

export function usePipelineStatus() {
  return useQuery({
    queryKey: ["pipeline-status"],
    queryFn: fetchPipelineStatus,
    refetchInterval: 30000,
  });
}
