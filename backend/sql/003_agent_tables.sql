CREATE TABLE agent_decisions (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL REFERENCES simulations(id) ON DELETE CASCADE,
    agent_id INTEGER REFERENCES agents(id),
    event_id INTEGER REFERENCES simulation_events(id),
    action VARCHAR(100),
    reason TEXT,
    confidence NUMERIC(5,2),
    estimated_cost NUMERIC(12,2),
    expected_impact TEXT,
    requires_approval BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'proposed',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE human_approvals (
    id SERIAL PRIMARY KEY,
    decision_id INTEGER NOT NULL REFERENCES agent_decisions(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending',
    responded_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE agent_memory (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL REFERENCES simulations(id) ON DELETE CASCADE,
    agent_id INTEGER REFERENCES agents(id),
    memory_type VARCHAR(100),
    content TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    decision_id INTEGER NOT NULL REFERENCES agent_decisions(id) ON DELETE CASCADE,
    strategic_score NUMERIC(5,2),
    financial_score NUMERIC(5,2),
    risk_score NUMERIC(5,2),
    overall_score NUMERIC(5,2),
    feedback TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);