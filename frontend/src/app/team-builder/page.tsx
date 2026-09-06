"use client";
import { useState } from "react";
import {
  DndContext,
  DragEndEvent,
  useDraggable,
  useDroppable,
} from "@dnd-kit/core";

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
  const style = transform
    ? { transform: `translate(${transform.x}px, ${transform.y}px)` }
    : undefined;

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="border rounded-lg p-3 mb-2 bg-white cursor-grab shadow-sm"
    >
      <p className="font-semibold">{agent.name}</p>
      <p className="text-sm text-gray-500">{agent.role}</p>
    </div>
  );
}

function TeamDropZone({ team }: { team: string[] }) {
  const { setNodeRef, isOver } = useDroppable({ id: "team-zone" });

  return (
    <div
      ref={setNodeRef}
      className={`min-h-[300px] border-2 border-dashed rounded-lg p-4 ${
        isOver ? "border-black bg-gray-50" : "border-gray-300"
      }`}
    >
      <p className="text-sm text-gray-500 mb-2">Your Team</p>
      {team.length === 0 && <p className="text-gray-400">Drop agents here</p>}
      {team.map((id) => {
        const agent = AVAILABLE_AGENTS.find((a) => a.id === id);
        return (
          <div key={id} className="border rounded-lg p-3 mb-2 bg-black text-white">
            {agent?.name} — {agent?.role}
          </div>
        );
      })}
    </div>
  );
}

export default function TeamBuilder() {
  const [team, setTeam] = useState<string[]>([]);

  function handleDragEnd(event: DragEndEvent) {
    const { over, active } = event;
    if (over?.id === "team-zone" && !team.includes(active.id as string)) {
      setTeam((prev) => [...prev, active.id as string]);
    }
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-6">Team Builder</h1>
      <DndContext onDragEnd={handleDragEnd}>
        <div className="grid grid-cols-2 gap-8">
          <div>
            <p className="text-sm text-gray-500 mb-2">Available Agents</p>
            {AVAILABLE_AGENTS.map((agent) => (
              <DraggableAgent key={agent.id} agent={agent} />
            ))}
          </div>
          <TeamDropZone team={team} />
        </div>
      </DndContext>

      {team.length > 0 && (
        <button className="mt-6 px-6 py-3 bg-black text-white rounded-lg">
          BUILD PRODUCT
        </button>
      )}
    </main>
  );
}