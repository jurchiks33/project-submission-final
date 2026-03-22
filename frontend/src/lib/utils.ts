export function cn(...values: Array<string | false | null | undefined>) {
  return values.filter(Boolean).join(" ");
}

export function pct(value: number, digits = 1) {
  return `${(value * 100).toFixed(digits)}%`;
}

export function num(value: number, digits = 2) {
  return value.toLocaleString(undefined, {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

export function money(value: number, digits = 2) {
  return `$${num(value, digits)}`;
}

export function fmtDate(value: string | null | undefined) {
  if (!value) return "N/A";
  return new Date(value).toLocaleString();
}
