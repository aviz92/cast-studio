#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# run_demo.sh  —  Generic demo recorder engine
#
# Usage (direct):
#   bash scripts/run_demo.sh [config_file]
#
# Usage (record with asciinema):
#   asciinema rec -c "bash scripts/run_demo.sh [config_file]" demo.cast
#
# Default config: scripts/demo.cfg
#
# Config file must define:
#   PROJECT, SUBTITLE, INSTALL_CMD, REPO_URL (optional: PYPI_URL)
#   define_runs()  — calls add_run() for each demo step
#
# Each run:
#   add_run "Title" "Desc line 1|Desc line 2" "command to execute"
#   (use | to separate multiple description lines)
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

CFG="${1:-scripts/demo.cfg}"

# ── defaults (overridden by config) ──────────────────────────────────────────
PROJECT="My Project"
SUBTITLE=""
INSTALL_CMD=""
REPO_URL=""
PYPI_URL=""
PAUSE_INTRO=2
PAUSE_BETWEEN=2
PAUSE_OUTRO=3

RUN_TITLES=()
RUN_DESCS=()
RUN_CMDS=()

add_run() {
  # add_run "Title" "Description (use | for multiple lines)" "shell command"
  RUN_TITLES+=("$1")
  RUN_DESCS+=("$2")
  RUN_CMDS+=("$3")
}

# ── load config ───────────────────────────────────────────────────────────────
[[ -f "$CFG" ]] || { echo "Config not found: $CFG"; exit 1; }
# shellcheck source=/dev/null
source "$CFG"
define_runs

# ── visual helpers ────────────────────────────────────────────────────────────
hr()    { printf '\n'; printf '\033[90m─%.0s\033[0m' {1..80}; printf '\n'; }
h1()    { printf '\n\033[1;36m  ▶  %s\033[0m\n\n' "$*"; }
dim()   { printf '\033[90m  %s\033[0m\n' "$*"; }
cmd_()  { printf '  \033[90m$\033[0m \033[33m%s\033[0m\n\n' "$*"; }
pause() { sleep "${1:-1.5}"; }

print_desc() {
  local desc="$1"
  IFS='|' read -ra lines <<< "$desc"
  for line in "${lines[@]}"; do
    [[ -n "$line" ]] && dim "$line"
  done
}

# ── INTRO ─────────────────────────────────────────────────────────────────────
clear
printf '\n'
printf '  \033[1;37m%s\033[0m' "$PROJECT"
[[ -n "$SUBTITLE" ]] && printf '  ·  \033[90m%s\033[0m' "$SUBTITLE"
printf '\n'
hr
[[ -n "$INSTALL_CMD" ]] && dim "$INSTALL_CMD"
[[ -n "$REPO_URL"    ]] && dim "$REPO_URL"
hr
pause "$PAUSE_INTRO"

# ── RUNS ──────────────────────────────────────────────────────────────────────
total="${#RUN_TITLES[@]}"

for i in "${!RUN_TITLES[@]}"; do
  n=$(( i + 1 ))
  clear
  h1 "${RUN_TITLES[$i]}"
  print_desc "${RUN_DESCS[$i]}"
  printf '\n'
  cmd_ "${RUN_CMDS[$i]}"
  pause 1.5

  # Run the command — allow failure so the demo continues even if tests fail
  eval "${RUN_CMDS[$i]}" || true

  [[ $n -lt $total ]] && pause "$PAUSE_BETWEEN"
done

pause "$PAUSE_BETWEEN"

# ── OUTRO ─────────────────────────────────────────────────────────────────────
clear
printf '\n'
hr
printf '  \033[1;36m%s\033[0m\n\n' "$PROJECT"
[[ -n "$INSTALL_CMD" ]] && printf '  \033[33m%s\033[0m\n'   "$INSTALL_CMD"
[[ -n "$REPO_URL"    ]] && printf '\n  \033[90m%s\033[0m\n' "$REPO_URL"
[[ -n "$PYPI_URL"    ]] && printf '  \033[90m%s\033[0m\n'   "$PYPI_URL"
hr
printf '\n'
pause "$PAUSE_OUTRO"
