#!/bin/bash
SCRIPT_DIR="$(realpath "$(dirname "$0")")"
PIPFILE_PATH="${SCRIPT_DIR}/Pipfile"
ENTRYPOINT="${SCRIPT_DIR}/openrouter_cli.py"
PIPENV_PIPFILE="$PIPFILE_PATH" pipenv -q run python "$ENTRYPOINT" "$@"
