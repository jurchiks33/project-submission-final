import type { ButtonHTMLAttributes, PropsWithChildren } from "react";
import { cn } from "../../lib/utils";

interface ButtonProps extends PropsWithChildren, ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
}

export function Button({ className, variant = "primary", children, ...props }: ButtonProps) {
  const base = "inline-flex items-center justify-center rounded-xl px-4 py-2.5 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50";
  const styles = {
    primary: "bg-accent text-slate-950 hover:bg-teal-300",
    secondary: "border border-border bg-panelAlt text-slate-100 hover:bg-slate-800",
    ghost: "text-slate-300 hover:bg-slate-800",
  };
  return (
    <button className={cn(base, styles[variant], className)} {...props}>
      {children}
    </button>
  );
}
