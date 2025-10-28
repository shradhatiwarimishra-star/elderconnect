#!/bin/bash

# Script to create database tables
# This is run automatically by docker-compose

echo "Waiting for PostgreSQL to be ready..."
sleep 5

echo "Creating database tables..."
python init_db.py

echo "Database setup complete!"
