export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return (
    <div className="rounded-2xl border border-border bg-panel p-8 text-center text-slate-400">
      <div className="mx-auto mb-3 h-6 w-6 animate-spin rounded-full border-2 border-slate-600 border-t-accent" />
      {label}
    </div>
  );
}
