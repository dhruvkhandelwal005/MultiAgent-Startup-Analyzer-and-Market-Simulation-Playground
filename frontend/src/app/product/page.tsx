"use client";

import { useEffect, useState } from "react";

type Product = {
  id: number;
  name: string;
  description: string;
  features: string[];
  pricing: number;
  quality_score: number;
  target_segments: string[];
};

export default function ProductView() {
  const [product, setProduct] = useState<Product | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/simulations/1/product")
      .then((res) => {
        if (!res.ok) throw new Error("Product not found");
        return res.json();
      })
      .then(setProduct)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-foreground">Product</h1>
        <p className="text-sm text-muted mt-1">
          The virtual product your agent team has built.
        </p>
      </div>

      {error && (
        <p className="text-sm text-danger border border-border p-4">{error}</p>
      )}

      {!product && !error && (
        <p className="text-sm text-muted">Loading product...</p>
      )}

      {product && (
        <div className="border border-border bg-surface max-w-2xl">
          <div className="p-6 border-b border-border">
            <h2 className="text-lg font-semibold text-foreground">{product.name}</h2>
            <p className="text-sm text-muted mt-1">{product.description}</p>
          </div>

          <div className="p-6 border-b border-border">
            <p className="text-xs text-muted uppercase tracking-wide mb-2">Features</p>
            <ul className="space-y-1">
              {product.features.map((f) => (
                <li key={f} className="text-sm text-foreground">
                  — {f}
                </li>
              ))}
            </ul>
          </div>

          <div className="grid grid-cols-2 border-b border-border">
            <div className="p-6 border-r border-border">
              <p className="text-xs text-muted uppercase tracking-wide">Price</p>
              <p className="font-mono text-xl mt-1 text-foreground">
                ₹{product.pricing}
              </p>
            </div>
            <div className="p-6">
              <p className="text-xs text-muted uppercase tracking-wide">
                Quality Score
              </p>
              <p className="font-mono text-xl mt-1 text-foreground">
                {product.quality_score}/100
              </p>
            </div>
          </div>

          <div className="p-6">
            <p className="text-xs text-muted uppercase tracking-wide mb-2">
              Target Segments
            </p>
            <div className="flex gap-2 flex-wrap">
              {product.target_segments.map((seg) => (
                <span
                  key={seg}
                  className="px-2.5 py-1 bg-accent-soft text-accent text-xs font-mono"
                >
                  {seg}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}