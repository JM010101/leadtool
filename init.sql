-- LeadTool Database Initialization
-- This file is executed when the PostgreSQL container starts

-- Create database if it doesn't exist
CREATE DATABASE leadtool;

-- Create user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'leadtool') THEN
        CREATE ROLE leadtool LOGIN PASSWORD 'password';
    END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE leadtool TO leadtool;

-- Connect to the database
\c leadtool;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO leadtool;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO leadtool;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO leadtool;
