import { Route, Routes } from "react-router-dom";
import { AppShell } from "./AppShell";
import { BacktestsPage } from "../pages/BacktestsPage";
import { DashboardPage } from "../pages/DashboardPage";
import { PositionsPage } from "../pages/PositionsPage";
import { SettingsPage } from "../pages/SettingsPage";
import { SignalsLogPage } from "../pages/SignalsLogPage";
import { TickerDetailPage } from "../pages/TickerDetailPage";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/signals" element={<SignalsLogPage />} />
        <Route path="/positions" element={<PositionsPage />} />
        <Route path="/backtests" element={<BacktestsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/ticker/:ticker" element={<TickerDetailPage />} />
      </Routes>
    </AppShell>
  );
}
