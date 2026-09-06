const METRICS = [
  { label: "Active Users", value: "—" },
  { label: "Revenue", value: "—" },
  { label: "Cash Remaining", value: "—" },
  { label: "Market Share", value: "—" },
];

export default function Dashboard() {
  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-foreground">Dashboard</h1>
        <p className="text-sm text-muted mt-1">
          Live overview of the simulation, product, and market.
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-border border border-border">
        {METRICS.map((m) => (
          <div key={m.label} className="bg-surface p-5">
            <p className="text-xs text-muted uppercase tracking-wide">{m.label}</p>
            <p className="font-mono text-2xl mt-2 text-foreground">{m.value}</p>
          </div>
        ))}
      </div>
    </main>
  );
}