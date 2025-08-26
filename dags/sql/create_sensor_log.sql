CREATE TABLE IF NOT EXISTS sensor_log (
    department_name VARCHAR(32) NOT NULL,
    sensor_serial VARCHAR(64) NOT NULL,
    create_at TIMESTAMP NOT NULL,
    product_name VARCHAR(16) NOT NULL,
    product_expire TIMESTAMP NOT NULL
);