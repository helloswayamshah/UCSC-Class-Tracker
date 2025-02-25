CREATE EXTENSION IF NOT EXISTS pgcrypto;

SELECT 'CREATE DATABASE "ClassTracker"'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ClassTracker')\gexec

\connect ClassTracker
CREATE EXTENSION IF NOT EXISTS pgcrypto;
