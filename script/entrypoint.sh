#!/bin/bash

set -e
# Exit immediately if any command fails (prevents silent errors)

# ------------------------------------------------------------
# Install Python dependencies
# ------------------------------------------------------------
if [ -e "/opt/airflow/requirements.txt" ]; then
  # Check if requirements.txt exists inside container

  python -m pip install --upgrade pip
  # Upgrade pip to latest version (best practice)

  pip install -r /opt/airflow/requirements.txt
  # Install all Python dependencies needed for DAGs (e.g., kafka-python)
fi

# ------------------------------------------------------------
# Initialize Airflow database (only first run)
# ------------------------------------------------------------
if [ ! -f "/opt/airflow/airflow.db" ]; then
  # If database file does NOT exist → first time startup

  airflow db init
  # Initialize Airflow metadata database (SQLite in this case)

  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
  # Create default admin user for Airflow UI
  # Access via http://localhost:8080
fi

# ------------------------------------------------------------
# Upgrade database schema
# ------------------------------------------------------------
airflow db upgrade
# Apply any pending database migrations (safe to run every time)

# ------------------------------------------------------------
# Start Airflow webserver
# ------------------------------------------------------------
exec airflow webserver
# Start the Airflow webserver
# 'exec' replaces this script process with the webserver process
# → ensures proper signal handling (Docker stop/restart works correctly)