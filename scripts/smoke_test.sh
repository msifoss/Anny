#!/usr/bin/env bash
# Smoke test: hit every Anny REST endpoint and report PASS/FAIL.
# Usage:
#   ./scripts/smoke_test.sh              # starts server automatically
#   ./scripts/smoke_test.sh --no-server  # use an already-running server
set -euo pipefail

BASE_URL="${ANNY_BASE_URL:-http://localhost:8000}"
NO_SERVER=false
SERVER_PID=""
PASS=0
FAIL=0

# --- Colors ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

# --- Parse args ---
for arg in "$@"; do
  case "$arg" in
    --no-server) NO_SERVER=true ;;
    *) echo "Unknown arg: $arg"; exit 1 ;;
  esac
done

# --- Cleanup ---
cleanup() {
  if [[ -n "$SERVER_PID" ]]; then
    echo ""
    echo "Stopping server (PID $SERVER_PID)..."
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# --- Validate env ---
check_env() {
  if [[ ! -f .env ]]; then
    echo -e "${RED}ERROR: .env file not found. Copy .env.example and configure it.${NC}"
    exit 1
  fi

  # Source .env to check key path
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a

  if [[ -z "${GOOGLE_SERVICE_ACCOUNT_KEY_PATH:-}" ]]; then
    echo -e "${RED}ERROR: GOOGLE_SERVICE_ACCOUNT_KEY_PATH not set in .env${NC}"
    exit 1
  fi

  if [[ ! -f "$GOOGLE_SERVICE_ACCOUNT_KEY_PATH" ]]; then
    echo -e "${RED}ERROR: Key file not found: $GOOGLE_SERVICE_ACCOUNT_KEY_PATH${NC}"
    exit 1
  fi
}

# --- Start server ---
start_server() {
  echo "Starting Anny server..."
  .venv/bin/uvicorn src.anny.main:app --host 0.0.0.0 --port 8000 &
  SERVER_PID=$!

  # Poll /health until ready (max 15 seconds)
  for i in $(seq 1 30); do
    if curl -sf "$BASE_URL/health" > /dev/null 2>&1; then
      echo -e "${GREEN}Server ready.${NC}"
      return
    fi
    sleep 0.5
  done
  echo -e "${RED}ERROR: Server failed to start within 15 seconds.${NC}"
  exit 1
}

# --- Test helpers ---
test_get() {
  local label="$1"
  local url="$2"
  local response
  local http_code

  http_code=$(curl -sf -o /dev/null -w "%{http_code}" "$url" 2>/dev/null) || http_code="000"
  response=$(curl -sf "$url" 2>/dev/null | head -c 200) || response="(no response)"

  if [[ "$http_code" == "200" ]]; then
    echo -e "  ${GREEN}PASS${NC}  $label  ${YELLOW}${response:0:120}${NC}"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}FAIL${NC}  $label  (HTTP $http_code)  ${YELLOW}${response:0:120}${NC}"
    FAIL=$((FAIL + 1))
  fi
}

test_post() {
  local label="$1"
  local url="$2"
  local body="$3"
  local http_code
  local response

  http_code=$(curl -sf -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$body" "$url" 2>/dev/null) || http_code="000"
  response=$(curl -sf -X POST -H "Content-Type: application/json" -d "$body" "$url" 2>/dev/null | head -c 200) || response="(no response)"

  if [[ "$http_code" == "200" ]]; then
    echo -e "  ${GREEN}PASS${NC}  $label  ${YELLOW}${response:0:120}${NC}"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}FAIL${NC}  $label  (HTTP $http_code)  ${YELLOW}${response:0:120}${NC}"
    FAIL=$((FAIL + 1))
  fi
}

# ===== Main =====
echo "=== Anny Smoke Test ==="
echo ""

check_env

if [[ "$NO_SERVER" == "false" ]]; then
  start_server
else
  echo "Using existing server at $BASE_URL"
fi

echo ""
echo "--- Health ---"
test_get "GET /health" "$BASE_URL/health"

echo ""
echo "--- GA4 ---"
test_get "GET /api/ga4/top-pages" "$BASE_URL/api/ga4/top-pages?date_range=last_28_days&limit=3"
test_get "GET /api/ga4/traffic-summary" "$BASE_URL/api/ga4/traffic-summary?date_range=last_28_days"
test_post "POST /api/ga4/report" "$BASE_URL/api/ga4/report" '{"metrics":"sessions","dimensions":"date","date_range":"last_28_days","limit":3}'

echo ""
echo "--- Search Console ---"
test_get "GET /api/search-console/top-queries" "$BASE_URL/api/search-console/top-queries?date_range=last_28_days&limit=3"
test_get "GET /api/search-console/top-pages" "$BASE_URL/api/search-console/top-pages?date_range=last_28_days&limit=3"
test_get "GET /api/search-console/summary" "$BASE_URL/api/search-console/summary?date_range=last_28_days"

echo ""
echo "--- Tag Manager ---"
test_get "GET /api/tag-manager/accounts" "$BASE_URL/api/tag-manager/accounts"

echo ""
echo "=== Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC} ==="

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
