"use client";

import { useEffect, useRef, useState } from "react";
import {
  closestCenter,
  DndContext,
  DragEndEvent,
  KeyboardSensor,
  PointerSensor,
  useDraggable,
  useDroppable,
  useSensor,
  useSensors,
} from "@dnd-kit/core";

type PopulationSegment = {
  id: number;
  segment_type: string;
  population_size: number;
  active_users: number;
};

type Competitor = {
  id: number;
  name: string;
  product_quality: number;
  price: number;
  market_share: number;
};

type MarketEntity = {
  dragId: string;
  label: string;
  type: "population" | "competitor";
};

function DraggableEntity({ entity }: { entity: MarketEntity }) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: entity.dragId,
  });
  const style = {
    touchAction: "none",
    ...(transform
      ? { transform: `translate(${transform.x}px, ${transform.y}px)` }
      : {}),
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="border border-border bg-surface p-3 mb-2 cursor-grab"
    >
      <p className="text-sm font-medium text-foreground">{entity.label}</p>
      <p className="text-xs text-muted capitalize">{entity.type}</p>
    </div>
  );
}

function MarketDropZone({ entities }: { entities: MarketEntity[] }) {
  const { setNodeRef, isOver } = useDroppable({ id: "market-zone" });

  return (
    <div
      ref={setNodeRef}
      className={`min-h-[260px] border border-dashed p-4 transition-colors ${
        isOver ? "border-accent bg-accent-soft" : "border-border"
      }`}
    >
      <p className="text-xs text-muted uppercase tracking-wide mb-2">
        Market
      </p>
      {entities.length === 0 && (
        <p className="text-sm text-muted">
          Drop a population group or competitor here to trigger a live agent
          response.
        </p>
      )}
      {entities.map((e) => (
        <div
          key={e.dragId}
          className="border border-border p-3 mb-2 bg-accent-soft text-accent text-sm font-mono"
        >
          {e.label} — {e.type}
        </div>
      ))}
    </div>
  );
}

export default function MarketPlayground() {
  const [population, setPopulation] = useState<PopulationSegment[]>([]);
  const [competitors, setCompetitors] = useState<Competitor[]>([]);
  const [marketEntities, setMarketEntities] = useState<MarketEntity[]>([]);
  const [activityLog, setActivityLog] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const logEndRef = useRef<HTMLDivElement>(null);
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 4 } }),
    useSensor(KeyboardSensor)
  );

  useEffect(() => {
    fetch("http://127.0.0.1:8000/simulations/1/population")
      .then((res) => res.json())
      .then(setPopulation)
      .catch(() => setPopulation([]));

    fetch("http://127.0.0.1:8000/simulations/1/competitors")
      .then((res) => res.json())
      .then(setCompetitors)
      .catch(() => setCompetitors([]));
  }, []);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activityLog]);

  const availableEntities: MarketEntity[] = [
    ...population.map((p) => ({
      dragId: `population-${p.id}`,
      label: p.segment_type,
      type: "population" as const,
    })),
    ...competitors.map((c) => ({
      dragId: `competitor-${c.id}`,
      label: c.name,
      type: "competitor" as const,
    })),
  ];

  async function runEvent(entity: MarketEntity) {
    setIsRunning(true);
    setActivityLog([`Event triggered: ${entity.label} entered the market.`]);

    const eventType = entity.type === "competitor" ? "general" : "general";
    const description =
      entity.type === "competitor"
        ? `New competitor "${entity.label}" entered the market.`
        : `New population segment "${entity.label}" added to the market.`;

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/simulations/1/events/stream",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            event_type: eventType,
            current_event: description,
          }),
        }
      );

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      if (!reader) throw new Error("No stream available");

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(6));
            if (data.message) {
              setActivityLog((prev) => [...prev, data.message]);
            }
            if (data.done) {
              const decision = data.result?.ceo_decision;
              if (decision) {
                setActivityLog((prev) => [
                  ...prev,
                  `Final: ${decision.action} (judge score: ${
                    decision.evaluation?.overall_score ?? "—"
                  }/100)`,
                ]);
              }
            }
          }
        }
      }
    } catch {
      setActivityLog((prev) => [...prev, "Error: could not reach backend."]);
    } finally {
      setIsRunning(false);
    }
  }

  function handleDragEnd(event: DragEndEvent) {
    const { over, active } = event;
    if (over?.id !== "market-zone") return;

    const entity = availableEntities.find((e) => e.dragId === active.id);
    if (!entity) return;
    if (marketEntities.find((e) => e.dragId === entity.dragId)) return;

    setMarketEntities((prev) => [...prev, entity]);
    if (!isRunning) runEvent(entity);
  }

  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-foreground">
          Market Playground
        </h1>
        <p className="text-sm text-muted mt-1">
          Drop a population segment or competitor to trigger a live agent
          response.
        </p>
      </div>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <div className="grid grid-cols-2 gap-6 mb-8">
          <div>
            <p className="text-xs text-muted uppercase tracking-wide mb-2">
              Available Entities
            </p>
            {availableEntities.length === 0 && (
              <p className="text-sm text-muted">Loading...</p>
            )}
            {availableEntities.map((entity) => (
              <DraggableEntity key={entity.dragId} entity={entity} />
            ))}
          </div>
          <MarketDropZone entities={marketEntities} />
        </div>
      </DndContext>

      <div className="border border-border bg-surface">
        <div className="px-4 py-3 border-b border-border flex items-center justify-between">
          <p className="text-xs text-muted uppercase tracking-wide">
            Agent Activity
          </p>
          {isRunning && (
            <span className="text-xs font-mono text-accent">running…</span>
          )}
        </div>
        <div className="p-4 h-64 overflow-y-auto font-mono text-sm space-y-1">
          {activityLog.length === 0 && (
            <p className="text-muted">
              No activity yet. Drop an entity above to start.
            </p>
          )}
          {activityLog.map((line, i) => (
            <p key={i} className="text-foreground">
              <span className="text-muted">{`>`}</span> {line}
            </p>
          ))}
          <div ref={logEndRef} />
        </div>
      </div>
    </main>
  );
}