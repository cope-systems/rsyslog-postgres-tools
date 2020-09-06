#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=common.sh
source "${SCRIPT_DIR}/common.sh"

run_tests(){
  start_database
  echo "Starting tests..."
  TEST_DATABASE_URL="postgres://postgres:${DATABASE_PASSWORD}@localhost:${DATABASE_PORT}/${DATABASE_NAME}" pytest --cov="${BASE_DIR}/rsyslog_postgres_tools" "${BASE_DIR}/test_rsyslog_postgres_tools"
  echo "Stopping tests..."
  stop_database
}

run_tests