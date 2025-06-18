#!/bin/bash
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
ENTRYPOINT="${SCRIPT_DIR}/openrouter_cli.py"
VENV_FILE="${SCRIPT_DIR}/.venv_path"
[ -f "${SCRIPT_DIR}/.env" ] && source "${SCRIPT_DIR}/.env"
if [ ! -f "${VENV_FILE}" ] ; then
  export PIPENV_PIPFILE="${SCRIPT_DIR}/Pipfile"
  pipenv -q --venv > "${VENV_FILE}"
fi
VENV_PATH=$(<"${VENV_FILE}")
[ ! -f "${VENV_PATH}/bin/python" ] && rm -f "${VENV_FILE}"
export OPENROUTER_API_KEY
exec "${VENV_PATH}/bin/python" "$ENTRYPOINT" "$@"
