import requests
from bs4 import BeautifulSoup

WATCHLIST = ["Georgia", "Kansas", "Oklahoma"]

def check_membership():
    url = "https://www.insurancecompact.org/regulator-resources/membership"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text()
    
    print("--- 2026 Election Watchdog Report ---")
    for state in WATCHLIST:
        if state in content:
            print(f"✅ {state} is confirmed in the [Membership Roster](https://www.insurancecompact.org/regulator-resources/membership)")
        else:
            print(f"⚠️ ALERT: {state} entry has changed!")

if __name__ == "__main__":
    check_membership()
