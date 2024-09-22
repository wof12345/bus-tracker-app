#!/bin/bash
set -e

# Create the database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE testdb;
EOSQL
