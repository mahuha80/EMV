#!/bin/bash
# ============================================================================
# QA Automation Pipeline – Jira to Robot Test Execution
# ============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "📋 QA Automation Pipeline"
echo "=========================="

# ── 0. Kiểm tra Prerequisites ─────────────────────────────────────────────
echo ""
echo "🔍 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install: brew install python3"
    exit 1
fi

if ! command -v robot &> /dev/null; then
    echo "❌ Robot Framework not installed. Running: pip3 install robotframework"
    python3 -m pip install robotframework --quiet
fi

if ! command -v mcp-atlassian &> /dev/null; then
    echo "❌ mcp-atlassian not installed. Running: npm install -g mcp-atlassian"
    npm install -g mcp-atlassian --silent
fi

# ── 1. Load .env ──────────────────────────────────────────────────────────
if [ ! -f .env ]; then
    echo "❌ .env file not found. Copy from .env.example or create one"
    exit 1
fi

source .env

if [ -z "$ATLASSIAN_BASE_URL" ] || [ -z "$ATLASSIAN_EMAIL" ] || [ -z "$ATLASSIAN_API_TOKEN" ]; then
    echo "❌ Missing Jira credentials in .env"
    exit 1
fi

echo "✅ Prerequisites OK"

# ── 2. Parse CommandLine Arguments ───────────────────────────────────────
TICKET=""
PLATFORM="android"
SKIP_TEST=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --ticket)   TICKET="$2"; shift 2 ;;
        --platform) PLATFORM="$2"; shift 2 ;;
        --skip-run) SKIP_TEST=true; shift ;;
        --dry-run)  DRY_RUN=true; shift ;;
        -h|--help)
            echo "Usage: $0 --ticket KAN-4 [--platform android|ios] [--skip-run] [--dry-run]"
            echo ""
            echo "Options:"
            echo "  --ticket KAN-4        • Jira ticket ID (bắt buộc)"
            echo "  --platform android    • Target platform: android (default) hoặc ios"
            echo "  --skip-run            • Chỉ fetch+parse+generate, không chạy Robot"
            echo "  --dry-run             • Generate .robot file và in ra stdout"
            exit 0
            ;;
        *)  echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$TICKET" ]; then
    echo "❌ Ticket ID required: $0 --ticket KAN-4"
    exit 1
fi

# ── 3. Run Python Pipeline ───────────────────────────────────────────────
echo ""
echo "🚀 Starting Pipeline for Ticket: $TICKET"
echo "   Platform: $PLATFORM"
echo ""

export PYTHONPATH="$PROJECT_ROOT/src"

if [ "$DRY_RUN" = true ]; then
    # Chỉ generate, không chạy Robot
    python3 src/jira_flow.py --ticket "$TICKET" --platform "$PLATFORM" 2>&1
    exit 0
fi

if [ "$SKIP_TEST" = true ]; then
    # Generate + skip Robot execution
    python3 src/jira_flow.py --ticket "$TICKET" --platform "$PLATFORM" --skip-run 2>&1
    exit 0
fi

# Full pipeline: fetch + parse + generate + run robot dryrun
python3 src/jira_flow.py --ticket "$TICKET" --platform "$PLATFORM" 2>&1

echo ""
echo "✅ Pipeline completed!"
echo ""
echo "📊 Reports:"
echo "   • Ticket data: reports/$TICKET/ticket_data.json"
echo "   • Robot suite: robot_tests/suites/generated/${TICKET}_${PLATFORM}.robot"
echo "   • Dryrun report: reports/$TICKET/robot_output/report.html"
echo ""
echo "🎬 Run actual tests (requires device + Appium server):"
echo "   robot robot_tests/suites/generated/${TICKET}_${PLATFORM}.robot"

