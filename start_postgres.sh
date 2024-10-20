#!/bin/bash

# Database is created on pgAdmin4 initially with below information
# Database connection details

TYPE="postgres"
HOST="localhost"
USER="postgres"
PASSWORD="Pp@639493"
PORT="5432"
DBNAME="DWH"
SCHEMA="public"

# Export the environment variables
export PGPASSWORD=$PASSWORD

# Start the PostgreSQL service (assuming it's already installed locally)
echo "Starting PostgreSQL server..."
sudo service postgresql start

# Verify the service is running
echo "Checking PostgreSQL service status..."
sudo service postgresql status

# Connect to PostgreSQL using psql
echo "Connecting to PostgreSQL server..."
psql -h $HOST -p $PORT -U $USER -d $DBNAME -c "SET search_path TO $SCHEMA;"

# Print success message
echo "PostgreSQL server is running and connected to database $DBNAME with schema $SCHEMA."
