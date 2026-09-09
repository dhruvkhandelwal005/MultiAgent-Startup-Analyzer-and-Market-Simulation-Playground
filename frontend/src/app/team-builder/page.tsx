"use client";

import { useState } from "react";
import {
  DndContext,
  DragEndEvent,
  PointerSensor,
  KeyboardSensor,
  closestCenter,
  useDraggable,
  useDroppable,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import { useRouter } from "next/navigation";

const AVAILABLE_AGENTS = [
  { id: "alex", name: "Alex", role: "CEO" },
  { id: "mark", name: "Mark", role: "Finance" },
  { id: "sam", name: "Sam", role: "Product" },
  { id: "denny", name: "Denny", role: "Developer" },
  { id: "mia", name: "Mia", role: "Marketing" },
];

function DraggableAgent({ agent }: { agent: (typeof AVAILABLE_AGENTS)[0] }) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: agent.id,
  });
  const style = {
    ...(transform
      ? { transform: `translate(${transform.x}px, ${transform.y}px)` }
      : {}),
    touchAction: "none" as const,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="border border-border bg-surface p-3 mb-2 cursor-grab"
    >
      <p className="text-sm font-medium text-foreground">{agent.name}</p>
      <p className="text-xs text-muted">{agent.role}</p>
    </div>
  );
}

function TeamDropZone({ team }: { team: string[] }) {
  const { setNodeRef, isOver } = useDroppable({ id: "team-zone" });

  return (
    <div
      ref={setNodeRef}
      className={`min-h-[260px] border border-dashed p-4 transition-colors ${
        isOver ? "border-accent bg-accent-soft" : "border-border"
      }`}
    >
      <p className="text-xs text-muted uppercase tracking-wide mb-2">
        Your Team
      </p>
      {team.length === 0 && (
        <p className="text-sm text-muted">Drop agents here</p>
      )}
      {team.map((id) => {
        const agent = AVAILABLE_AGENTS.find((a) => a.id === id);
        return (
          <div
            key={id}
            className="border border-border p-3 mb-2 bg-accent-soft text-accent text-sm font-mono"
          >
            {agent?.name} — {agent?.role}
          </div>
        );
      })}
    </div>
  );
}

export default function TeamBuilder() {
  const [team, setTeam] = useState<string[]>([]);
  const [idea, setIdea] = useState("");
  const [budget, setBudget] = useState("1000000");
  const [isBuilding, setIsBuilding] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 4 } }),
    useSensor(KeyboardSensor)
  );

  function handleDragEnd(event: DragEndEvent) {
    const { over, active } = event;
    if (over?.id === "team-zone" && !team.includes(active.id as string)) {
      setTeam((prev) => [...prev, active.id as string]);
    }
  }

  async function handleBuild() {
    if (!idea.trim()) {
      setError("Describe your product idea first.");
      return;
    }
    setError(null);
    setIsBuilding(true);
    try {
      await fetch("http://127.0.0.1:8000/simulations/1/team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agent_roles: team.map(
            (id) => AVAILABLE_AGENTS.find((a) => a.id === id)?.role.toLowerCase() ?? ""
          ),
        }),
      });

      const res = await fetch(
        "http://127.0.0.1:8000/simulations/1/build-product",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            idea,
            budget: parseFloat(budget) || 1000000,
          }),
        }
      );
      if (!res.ok) throw new Error("Failed to build product");
      router.push("/product");
    } catch {
      setError("Could not build product. Is the backend running?");
    } finally {
      setIsBuilding(false);
    }
  }

  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-foreground">
          Team Builder
        </h1>
        <p className="text-sm text-muted mt-1">
          Pick your agent team, describe your idea, and let them build the
          product.
        </p>
      </div>

      <div className="mb-8 border border-border bg-surface p-5 max-w-2xl">
        <label className="block text-xs text-muted uppercase tracking-wide mb-2">
          Product Idea
        </label>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder="e.g. An AI-powered fitness coaching app for busy professionals"
          className="w-full border border-border bg-background p-3 text-sm text-foreground mb-4 resize-none h-20 focus:outline-none focus:border-accent"
        />
        <label className="block text-xs text-muted uppercase tracking-wide mb-2">
          Initial Budget (₹)
        </label>
        <input
          type="number"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
          className="w-full border border-border bg-background p-3 text-sm font-mono text-foreground focus:outline-none focus:border-accent"
        />
      </div>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <div className="grid grid-cols-2 gap-6">
          <div>
            <p className="text-xs text-muted uppercase tracking-wide mb-2">
              Available Agents
            </p>
            {AVAILABLE_AGENTS.map((agent) => (
              <DraggableAgent key={agent.id} agent={agent} />
            ))}
          </div>
          <TeamDropZone team={team} />
        </div>
      </DndContext>

      {error && <p className="text-sm text-danger mt-4">{error}</p>}

      {team.length > 0 && (
        <button
          onClick={handleBuild}
          disabled={isBuilding}
          className="mt-6 px-6 py-3 bg-accent text-white text-sm font-medium disabled:opacity-50"
        >
          {isBuilding ? "Building product…" : "BUILD PRODUCT"}
        </button>
      )}
    </main>
  );
}