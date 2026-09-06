CREATE TABLE population_groups (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL REFERENCES simulations(id) ON DELETE CASCADE,
    segment_type VARCHAR(100) NOT NULL,
    population_size INTEGER NOT NULL,
    product_relevance NUMERIC(5,2) DEFAULT 50,
    purchasing_power NUMERIC(5,2) DEFAULT 50,
    awareness NUMERIC(5,2) DEFAULT 0,
    adoption_rate NUMERIC(5,2) DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE competitors (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL REFERENCES simulations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    product_quality NUMERIC(5,2) DEFAULT 50,
    price NUMERIC(10,2),
    marketing_strength NUMERIC(5,2) DEFAULT 50,
    market_share NUMERIC(5,2) DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE marketing_actions (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL REFERENCES simulations(id) ON DELETE CASCADE,
    campaign_name VARCHAR(255) NOT NULL,
    target_segment_id INTEGER REFERENCES population_groups(id),
    budget NUMERIC(12,2) NOT NULL,
    expected_reach INTEGER,
    expected_conversion NUMERIC(5,2),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE simulation_events (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL REFERENCES simulations(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    description TEXT,
    payload JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE metrics_snapshots (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL REFERENCES simulations(id) ON DELETE CASCADE,
    total_population INTEGER,
    active_users INTEGER,
    revenue NUMERIC(14,2),
    expenses NUMERIC(14,2),
    cash_remaining NUMERIC(14,2),
    market_share NUMERIC(5,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);