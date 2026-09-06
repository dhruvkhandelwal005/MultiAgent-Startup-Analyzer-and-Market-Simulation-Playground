"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/team-builder", label: "Team Builder" },
  { href: "/product", label: "Product" },
  { href: "/market", label: "Market" },
];

export default function TopNav() {
  const pathname = usePathname();

  return (
    <header className="border-b border-border bg-surface">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
        <span className="text-sm font-mono tracking-tight text-foreground">
          market-sim<span className="text-muted">/control-room</span>
        </span>
        <nav className="flex gap-1">
          {LINKS.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-1.5 text-sm rounded-none border-b-2 transition-colors ${
                  active
                    ? "border-accent text-accent"
                    : "border-transparent text-muted hover:text-foreground"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}