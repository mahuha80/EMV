"""
Script tạo 3 sample tickets lên Jira KAN project
Chạy: python3 scripts/create_sample_tickets.py
"""
import os, sys, requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("ATLASSIAN_BASE_URL", "").rstrip("/")
EMAIL    = os.getenv("ATLASSIAN_EMAIL", "")
TOKEN    = os.getenv("ATLASSIAN_API_TOKEN", "")
PROJECT  = "KAN"
AUTH     = (EMAIL, TOKEN)
HEADERS  = {"Accept": "application/json", "Content-Type": "application/json"}


# ── ADF Helpers ───────────────────────────────────────────────────────────────

def h3(text):
    return {"type": "heading", "attrs": {"level": 3},
            "content": [{"type": "text", "text": text}]}

def bullets(items):
    return {"type": "bulletList", "content": [
        {"type": "listItem", "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": it}]}
        ]} for it in items
    ]}

def ordered(items):
    return {"type": "orderedList", "content": [
        {"type": "listItem", "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": it}]}
        ]} for it in items
    ]}

def doc(*content):
    return {"type": "doc", "version": 1, "content": list(content)}


# ── 3 Sample Tickets ──────────────────────────────────────────────────────────

TICKETS = [
    {
        "summary": "[Android] Login screen crashes when tapping Login with empty password field",
        "issuetype": "Bug",
        "priority": "High",
        "labels": ["android", "regression", "P1"],
        "description": doc(
            h3("Preconditions"),
            bullets([
                "App is installed on Android device (API 31+)",
                "User is on the Login screen (not logged in)",
                "App is in fresh install state (no active session)",
            ]),
            h3("Steps to Reproduce"),
            ordered([
                "Launch the application",
                "Wait for Login screen to appear",
                "Enter a valid email address: testuser@company.com",
                "Leave the Password field EMPTY (do not type anything)",
                "Tap the Login button",
            ]),
            h3("Expected Result"),
            bullets([
                'App displays validation message: "Password cannot be empty"',
                "App must NOT crash or force close",
                "User remains on the Login screen",
                "Error message is clearly visible below the Password field",
            ]),
            h3("Actual Result"),
            bullets([
                "App crashes immediately with force close dialog",
                'Dialog shows: "App has stopped"',
                "User is forced back to the device home screen",
            ]),
        ),
    },
    {
        "summary": "[iOS] Profile photo upload shows no progress indicator on slow network",
        "issuetype": "Bug",
        "priority": "Medium",
        "labels": ["ios", "android", "regression", "P2"],
        "description": doc(
            h3("Preconditions"),
            bullets([
                "User is logged in successfully",
                "User is on the Profile screen",
                "Device is on slow network (3G or throttled)",
            ]),
            h3("Steps to Reproduce"),
            ordered([
                "Tap on the avatar icon on the Profile screen",
                'Select "Change Photo" from the bottom sheet menu',
                "Choose a photo from the gallery (size > 2MB)",
                'Tap "Confirm" to start the upload',
                "Observe the UI during the upload process",
            ]),
            h3("Expected Result"),
            bullets([
                "A progress bar/spinner is displayed during upload",
                "App does NOT freeze or timeout without user feedback",
                'On success: toast message "Photo updated successfully"',
                "On failure: Retry button displayed with clear error message",
                "App remains responsive throughout the upload",
            ]),
            h3("Actual Result"),
            bullets([
                "No progress indicator shown",
                "App freezes ~30 seconds then returns to Profile screen silently",
                "No success or error message shown to user",
            ]),
        ),
    },
    {
        "summary": "[Feature] Add biometric authentication (Face ID / Fingerprint) to Login screen",
        "issuetype": "Story",
        "priority": "High",
        "labels": ["android", "ios", "feature", "smoke"],
        "description": doc(
            h3("Preconditions"),
            bullets([
                "User has a valid account in the system",
                "Device has biometric authentication enabled (Face ID or Fingerprint)",
                "User is not logged in (on the Login screen)",
            ]),
            h3("Steps to Reproduce"),
            ordered([
                "Launch the app and navigate to Login screen",
                'Tap "Login with Biometric" button (Face ID / Touch ID)',
                "Perform biometric authentication when prompted",
                "Observe the result",
            ]),
            h3("Expected Result"),
            bullets([
                '"Login with Biometric" button visible on Login screen',
                "System prompts biometric scan (Face ID or Fingerprint)",
                "On success: auto login and navigate to Home screen",
                "On failure/cancel: error message shown, remain on Login screen",
                "Biometric login works on Android (Fingerprint) and iOS (Face ID/Touch ID)",
            ]),
        ),
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_issuetype_id(name: str) -> str:
    r = requests.get(f"{BASE_URL}/rest/api/3/project/{PROJECT}",
                     auth=AUTH, headers={"Accept": "application/json"})
    for it in r.json().get("issueTypes", []):
        if it["name"].lower() == name.lower():
            return it["id"]
    return "10007"


def create_ticket(ticket: dict) -> dict:
    payload = {
        "fields": {
            "project":     {"key": PROJECT},
            "issuetype":   {"id": get_issuetype_id(ticket["issuetype"])},
            "summary":     ticket["summary"],
            "description": ticket["description"],
            "priority":    {"name": ticket["priority"]},
            "labels":      ticket["labels"],
        }
    }
    return requests.post(f"{BASE_URL}/rest/api/3/issue",
                         auth=AUTH, headers=HEADERS, json=payload).json()


def main():
    if not all([BASE_URL, EMAIL, TOKEN]):
        print("❌ Thiếu credentials trong .env"); sys.exit(1)

    print(f"🚀 Tạo {len(TICKETS)} tickets lên project [{PROJECT}] tại {BASE_URL}\n")
    created = []

    for i, ticket in enumerate(TICKETS, 1):
        print(f"  [{i}/{len(TICKETS)}] {ticket['summary'][:65]}...")
        result = create_ticket(ticket)
        if "key" in result:
            key = result["key"]
            url = f"{BASE_URL}/browse/{key}"
            print(f"         ✅ {key} → {url}")
            created.append({"key": key, "url": url})
        else:
            print(f"         ❌ Failed: {result}")

    print(f"\n{'='*65}")
    print(f"✅ {len(created)}/{len(TICKETS)} tickets created\n")
    for c in created:
        print(f"  🎫 {c['key']} → {c['url']}")

    if created:
        first = created[0]["key"]
        print(f"\n▶ Test flow ngay:")
        print(f"  PYTHONPATH=src python3 src/flow_runner.py --ticket {first} --skip-run")


if __name__ == "__main__":
    main()
