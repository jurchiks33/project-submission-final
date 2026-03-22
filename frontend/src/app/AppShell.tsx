import type { PropsWithChildren } from "react";
import { PageHeader } from "../components/PageHeader";

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen px-4 py-6 md:px-8">
      <div className="mx-auto max-w-7xl">
        <PageHeader />
        {children}
      </div>
    </div>
  );
}
