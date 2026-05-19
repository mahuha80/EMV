#!/usr/bin/env python3
"""Test STEP 3: Generate Robot Framework tests"""

import json
from pathlib import Path
from src.testing.test_case_mapper import TestCaseMapper

def main():
    # Load ticket data và analysis
    ticket_data = json.loads(Path("reports/KAN-7/ticket_data.json").read_text())
    analysis = json.loads(Path("reports/KAN-7/ticket_analysis.json").read_text())

    print("=" * 80)
    print("📝 STEP 3: GENERATING ROBOT FRAMEWORK TESTS")
    print("=" * 80)
    print()
    print(f"Ticket: {ticket_data['ticket_id']}")
    print(f"Test Type: {analysis.get('test_type', 'N/A')}")
    print(f"Platforms: {analysis.get('platforms', [])}")
    print()

    # Generate tests for each platform
    results = []
    for platform in analysis.get('platforms', ['android']):
        print(f"🔧 Generating tests for {platform}...")
        mapper = TestCaseMapper(platform=platform, dry_run=False)
        suite_path, test_cases = mapper.generate(ticket_data, analysis)
        results.append({
            'platform': platform,
            'suite_path': str(suite_path),
            'test_count': len(test_cases)
        })
        print(f"   ✅ Suite: {suite_path}")
        print(f"   ✅ Test cases: {len(test_cases)}")
        print()

    print("=" * 80)
    print("✅ STEP 3 COMPLETE!")
    print("=" * 80)
    for r in results:
        print(f"  {r['platform']}: {r['test_count']} tests → {r['suite_path']}")
    print()

if __name__ == "__main__":
    main()

