import threading
import time
import json
import requests
import platform
from checks.system_health import get_system_health_snapshot


CHECK_INTERVAL_SECONDS = 1800  # 30 minutes
STATE_FILE = "last_state.json"
API_ENDPOINT = "https://your-api.com/update"  # Replace with your actual endpoint

def load_last_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def states_differ(state1, state2):
    return state1 != state2

def report_state(state):
    try:
        # response = requests.post(API_ENDPOINT, json=state)
        # print(f"✅ Reported update: {response.status_code}")
        print("hehe")
    except Exception as e:
        print(f"❌ Failed to report state: {e}")

def check_and_report():
    current_state = get_system_health_snapshot()
    last_state = load_last_state()

    if last_state is None or states_differ(current_state, last_state):
        print("🔄 Change detected. Reporting...")
        report_state(current_state)
        save_state(current_state)
    else:
        print("✅ No changes detected.")

    # Schedule next check as a daemon
    t = threading.Timer(CHECK_INTERVAL_SECONDS, check_and_report)
    t.daemon = True
    t.start()


def start_daemon():
    print(f"🚀 Starting daemon on {platform.system()}...")
    check_and_report()

if __name__ == "__main__":
    start_daemon()
