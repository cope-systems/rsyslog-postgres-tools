BASE_DIR="$(dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )")"
DATABASE_CONTAINER_NAME=rsyslog-postgres-tools-test-db
DATABASE_NAME=rsyslog_postgres_tools
DATABASE_PASSWORD=docker
DATABASE_PORT=
DATABASE_RUNNING=0
HTTP_PORT=
OLD_DIR="$(pwd)"


get_version(){
  cat "${BASE_DIR}/VERSION"
}

return_to_old_dir(){
  cd "${OLD_DIR}" || return
}

# shellcheck disable=SC2120
build(){
  cd "${BASE_DIR}" || return
  local tag
  local image_name="${2:-rsyslog-postgres-tools}"
  local version
  version="$(get_version)"
  tag="${1:-"${image_name}:${version}"}"
  echo "Building ${tag}"
  docker build -t "${tag}" .
}

run_untagged(){
  cd "${BASE_DIR}" || return
  HTTP_PORT="$(( RANDOM % 3000 + 2000))"
  echo "Port ${HTTP_PORT} mapped to port 8080 in container"

  # Bad hack to work around the fact default bind host is to 127.0.0.1,
  # which we probably don't want running in a container
  if [[ "$*" =~ .*run_http_server.* ]]; then
    docker run -p "${HTTP_PORT}:8080" -it "$(docker build -q .)" "/app/run_rp_tools.py" "$@" -b 0.0.0.0
  else
    docker run -p "${HTTP_PORT}:8080" -it "$(docker build -q .)" "/app/run_rp_tools.py" "$@"
  fi


}


stop_database(){
  if [[ ${DATABASE_RUNNING} -eq 1 ]]; then
    echo "Stopping database..."
    docker stop "${DATABASE_CONTAINER_NAME}"
    echo "Database stopped successfully.."
    DATABASE_RUNNING=0
  fi
}

on_exit(){
  return_to_old_dir
  stop_database
}

trap on_exit EXIT

run_sql(){
  local command=$1
  local database="${2:-postgres}"
  docker exec -e PGPASSWORD="${DATABASE_PASSWORD}" "${DATABASE_CONTAINER_NAME}" psql --username=postgres "${database}" -c "${command}"
}

# shellcheck disable=SC2120
start_database(){
  if [[ ${DATABASE_RUNNING} -eq 0 ]]; then
    docker pull postgres
    DATABASE_PORT="${1:-$(( RANDOM % 3000 + 2000))}"
    echo "Starting database mapped to port ${DATABASE_PORT}"
    docker run --rm --name "${DATABASE_CONTAINER_NAME}" -e POSTGRES_PASSWORD="${DATABASE_PASSWORD}" -d -p "${DATABASE_PORT}:5432" postgres
    DATABASE_RUNNING=1
    echo "Database started successfully."
    echo "Initializing database..."
    # If we try to run this too fast, the database won't be ready
    sleep 2
    run_sql "CREATE DATABASE ${DATABASE_NAME};" "postgres"
  fi
}
