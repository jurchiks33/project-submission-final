import { Link, useLocation } from "react-router-dom";
import { Card } from "./ui/Card";
import { cn } from "../lib/utils";

const nav = [
  { label: "Dashboard", to: "/" },
  { label: "Signals", to: "/signals" },
  { label: "Positions", to: "/positions" },
  { label: "Backtests", to: "/backtests" },
  { label: "Settings", to: "/settings" },
];

export function PageHeader() {
  const location = useLocation();
  return (
    <Card className="sticky top-0 z-10 mb-6 border-slate-800/80 bg-slate-950/80 py-4">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-accent/80">Trading Advisor Bot</p>
          <h1 className="mt-2 text-3xl font-semibold text-slate-50">After-close decision support dashboard</h1>
        </div>
        <nav className="flex flex-wrap gap-2">
          {nav.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "rounded-full px-4 py-2 text-sm transition",
                location.pathname === item.to
                  ? "bg-accent text-slate-950"
                  : "bg-panelAlt text-slate-300 hover:bg-slate-800",
              )}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </Card>
  );
}
