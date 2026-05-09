#!/usr/bin/env bash
set -euo pipefail

# Create a local development checkout and Python virtual environment for the
# canonical the-aisle repository only.
#
# Usage:
#   scripts/setup_the_aisle_env.sh [CHECKOUT_DIR] [ENV_DIR]
#
# CHECKOUT_DIR defaults to ./the-aisle at this repository root.
# ENV_DIR defaults to <CHECKOUT_DIR>/.venv-the-aisle.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST_REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
THE_AISLE_REPO_URL="https://github.com/seanyofthedead/the-aisle"
CHECKOUT_DIR="${1:-${HOST_REPO_ROOT}/the-aisle}"
ENV_DIR="${2:-${CHECKOUT_DIR}/.venv-the-aisle}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

normalize_repo_url() {
  local url="$1"
  url="${url%.git}"
  printf '%s' "${url}"
}

ensure_the_aisle_checkout() {
  if [[ -d "${CHECKOUT_DIR}/.git" ]]; then
    local origin_url
    origin_url="$(git -C "${CHECKOUT_DIR}" config --get remote.origin.url)"

    if [[ "$(normalize_repo_url "${origin_url}")" != "$(normalize_repo_url "${THE_AISLE_REPO_URL}")" ]]; then
      cat >&2 <<MESSAGE
Refusing to update ${CHECKOUT_DIR} because its origin is not the approved repo.
Expected: ${THE_AISLE_REPO_URL}
Actual:   ${origin_url}
MESSAGE
      exit 1
    fi

    local branch
    branch="$(git -C "${CHECKOUT_DIR}" rev-parse --abbrev-ref HEAD)"
    git -C "${CHECKOUT_DIR}" pull --ff-only origin "${branch}"
  elif [[ -e "${CHECKOUT_DIR}" ]]; then
    echo "Refusing to overwrite non-git path: ${CHECKOUT_DIR}" >&2
    exit 1
  else
    git clone "${THE_AISLE_REPO_URL}" "${CHECKOUT_DIR}"
  fi
}

install_repo_requirements() {
  local requirements_file="${CHECKOUT_DIR}/requirements.txt"

  "${PYTHON_BIN}" -m venv --prompt the-aisle "${ENV_DIR}"
  "${ENV_DIR}/bin/python" -m pip install --upgrade pip

  if [[ -f "${requirements_file}" ]]; then
    "${ENV_DIR}/bin/python" -m pip install -r "${requirements_file}"
  else
    echo "No requirements.txt found in ${CHECKOUT_DIR}; skipping dependency install."
  fi
}

ensure_the_aisle_checkout
install_repo_requirements

cat <<MESSAGE

Created the the-aisle checkout and environment.

Repository:
  ${CHECKOUT_DIR}

Environment:
  ${ENV_DIR}

Source repository locked to:
  ${THE_AISLE_REPO_URL}

Activate it with:
  source "${ENV_DIR}/bin/activate"
MESSAGE
