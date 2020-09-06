#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=common.sh
source "${SCRIPT_DIR}/common.sh"

OLD_DIR="$(pwd)"

return_to_old_dir(){
  cd "${OLD_DIR}"
}

trap return_to_old_dir EXIT

# shellcheck disable=SC2120
run_containerized(){
  run_untagged "$@"
}

run_containerized "$@"