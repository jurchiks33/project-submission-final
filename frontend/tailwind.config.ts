import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#090b10",
        panel: "#11151d",
        panelAlt: "#171d28",
        border: "#243042",
        accent: "#4fd1c5",
        signal: {
          enter: "#22c55e",
          exit: "#f97316",
          hold: "#38bdf8",
          flat: "#94a3b8",
          blocked: "#ef4444",
        },
      },
      boxShadow: {
        panel: "0 18px 48px rgba(0, 0, 0, 0.28)",
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
} satisfies Config;
