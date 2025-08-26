CREATE TABLE IF NOT EXISTS sensor_log (
    department_name VARCHAR(32) NOT NULL,
    sensor_serial VARCHAR(64) NOT NULL,
    create_at DATE NOT NULL,
    product_name VARCHAR(16) NOT NULL,
    product_expire DATE NOT NULL
);

-- CREATE INDEX IF NOT EXISTS idx_sensor_log_department_name ON sensor_log(department_name);
-- CREATE INDEX IF NOT EXISTS idx_sensor_log_sensor_serial ON sensor_log(sensor_serial);
-- CREATE INDEX IF NOT EXISTS idx_sensor_log_create_at ON sensor_log(create_at);
-- CREATE INDEX IF NOT EXISTS idx_sensor_log_product_name ON sensor_log(product_name);
-- CREATE INDEX IF NOT EXISTS idx_sensor_log_product_expire ON sensor_log(product_expire);