"use client";

import { useEffect, useState } from "react";

type Metrics = {
  total_population: number;
  active_users: number;
  revenue: number;
  expenses: number;
  cash_remaining: number;
  market_share: number;
};

export default function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/simulations/1/metrics")
      .then((res) => {
        if (!res.ok) throw new Error("No metrics found");
        return res.json();
      })
      .then(setMetrics)
      .catch((err) => setError(err.message));
  }, []);

  const cards = metrics
    ? [
        { label: "Active Users", value: metrics.active_users.toLocaleString() },
        { label: "Revenue", value: `₹${metrics.revenue.toLocaleString()}` },
        {
          label: "Cash Remaining",
          value: `₹${metrics.cash_remaining.toLocaleString()}`,
        },
        { label: "Market Share", value: `${metrics.market_share}%` },
      ]
    : [
        { label: "Active Users", value: "—" },
        { label: "Revenue", value: "—" },
        { label: "Cash Remaining", value: "—" },
        { label: "Market Share", value: "—" },
      ];

  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-foreground">Dashboard</h1>
        <p className="text-sm text-muted mt-1">
          Live overview of the simulation, product, and market.
        </p>
      </div>

      {error && (
        <p className="text-sm text-danger border border-border p-4 mb-6">
          {error}
        </p>
      )}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-border border border-border">
        {cards.map((m) => (
          <div key={m.label} className="bg-surface p-5">
            <p className="text-xs text-muted uppercase tracking-wide">
              {m.label}
            </p>
            <p className="font-mono text-2xl mt-2 text-foreground">
              {m.value}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}