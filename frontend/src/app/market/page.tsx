"use client";
import { useState } from "react";
import {
  DndContext,
  DragEndEvent,
  useDraggable,
  useDroppable,
} from "@dnd-kit/core";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

const AVAILABLE_ENTITIES = [
  { id: "doctors", name: "Doctors", type: "population" },
  { id: "students", name: "Students", type: "population" },
  { id: "tech_workers", name: "Tech Workers", type: "population" },
  { id: "competitor_a", name: "Competitor A", type: "competitor" },
  { id: "competitor_b", name: "Competitor B", type: "competitor" },
];

function DraggableEntity({ entity }: { entity: (typeof AVAILABLE_ENTITIES)[0] }) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({ id: entity.id });
  const style = transform
    ? { transform: `translate(${transform.x}px, ${transform.y}px)` }
    : undefined;

  const bg = entity.type === "population" ? "bg-white" : "bg-yellow-50";

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className={`border rounded-lg p-3 mb-2 cursor-grab shadow-sm ${bg}`}
    >
      <p className="font-semibold">{entity.name}</p>
      <p className="text-sm text-gray-500 capitalize">{entity.type}</p>
    </div>
  );
}

function MarketDropZone({ entities }: { entities: string[] }) {
  const { setNodeRef, isOver } = useDroppable({ id: "market-zone" });

  return (
    <div
      ref={setNodeRef}
      className={`min-h-[300px] border-2 border-dashed rounded-lg p-4 ${
        isOver ? "border-black bg-gray-50" : "border-gray-300"
      }`}
    >
      <p className="text-sm text-gray-500 mb-2">Market</p>
      {entities.length === 0 && <p className="text-gray-400">Drop population groups or competitors here</p>}
      {entities.map((id) => {
        const entity = AVAILABLE_ENTITIES.find((e) => e.id === id);
        return (
          <div key={id} className="border rounded-lg p-3 mb-2 bg-black text-white">
            {entity?.name} — {entity?.type}
          </div>
        );
      })}
    </div>
  );
}

// Dummy metrics history — will be replaced by real backend data later
const dummyMetrics = [
  { time: "T0", users: 0 },
  { time: "T1", users: 200 },
  { time: "T2", users: 550 },
  { time: "T3", users: 900 },
];

export default function MarketPlayground() {
  const [marketEntities, setMarketEntities] = useState<string[]>([]);

  function handleDragEnd(event: DragEndEvent) {
    const { over, active } = event;
    if (over?.id === "market-zone" && !marketEntities.includes(active.id as string)) {
      setMarketEntities((prev) => [...prev, active.id as string]);
    }
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-6">Market Playground</h1>

      <DndContext onDragEnd={handleDragEnd}>
        <div className="grid grid-cols-2 gap-8 mb-8">
          <div>
            <p className="text-sm text-gray-500 mb-2">Available Entities</p>
            {AVAILABLE_ENTITIES.map((entity) => (
              <DraggableEntity key={entity.id} entity={entity} />
            ))}
          </div>
          <MarketDropZone entities={marketEntities} />
        </div>
      </DndContext>

      <div className="border rounded-lg p-4">
        <p className="text-sm text-gray-500 mb-2">Active Users Over Time (dummy data)</p>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={dummyMetrics}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="users" stroke="#000000" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </main>
  );
}