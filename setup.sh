#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "Node.js/npm is required."; exit 1; }
if [ ! -d .venv ]; then python3 -m venv .venv; fi
if [ -f .venv/bin/activate ]; then source .venv/bin/activate; else source .venv/Scripts/activate; fi
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
(cd frontend && npm install)
if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example"; fi
printf '\nDependencies installed. Starting TripWise...\n'
(uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000) & API_PID=$!
cleanup() { kill "$API_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
(cd frontend && npm run dev -- --host 0.0.0.0)
