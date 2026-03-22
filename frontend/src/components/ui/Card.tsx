import type { PropsWithChildren } from "react";
import { cn } from "../../lib/utils";

interface CardProps extends PropsWithChildren {
  className?: string;
}

export function Card({ className, children }: CardProps) {
  return (
    <div className={cn("rounded-2xl border border-border bg-panel/90 p-5 shadow-panel backdrop-blur", className)}>
      {children}
    </div>
  );
}
