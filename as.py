import requests
import re
import json

# Sony API URL (same as Worker)
TARGET_API = "https://apiv2.sonyliv.com/AGL/1.5/A/ENG/WEB/IN/CONTENT/VIDEOURL/VOD/1090491205/freepreview"

# Optional: headers to mimic browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

try:
    resp = requests.get(TARGET_API, headers=HEADERS, timeout=10)
    resp.raise_for_status()
except requests.RequestException as e:
    print("Error fetching API:", e)
    exit(1)

try:
    data = resp.json()
except json.JSONDecodeError:
    print("Failed to decode JSON")
    exit(1)

# Extract videoURL and hdnea token
videoURL = data.get("resultObj", {}).get("videoURL")
hdnea = None
if videoURL:
    match = re.search(r"hdnea=([^&]+)", videoURL)
    if match:
        hdnea = match.group(1)

# Save to as.txt
with open("as.txt", "w") as f:
    f.write(f"hdnea: {hdnea}\n")

print("Saved token to as.txt")
print(f"videoURL: {videoURL}")
print(f"hdnea: {hdnea}")
