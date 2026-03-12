CREATE TABLE t_p29589758_quantum_tech_initiat.co2_measurements (
    id SERIAL PRIMARY KEY,
    value NUMERIC(10, 2) NOT NULL,
    unit VARCHAR(10) NOT NULL DEFAULT 'ppm',
    location VARCHAR(255),
    sensor_id VARCHAR(100),
    measured_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);