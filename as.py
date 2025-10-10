import requests
import json
from datetime import datetime

# Sony API endpoint (example: freepreview/video)
SONY_API_URL = "https://apiv2.sonyliv.com/AGL/1.5/A/ENG/WEB/IN/CONTENT/VIDEOURL/VOD/1090491205/freepreview"

# Output file
OUTPUT_FILE = "as.txt"

def fetch_token():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/141.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
    }

    try:
        resp = requests.get(SONY_API_URL, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # Check for videoURL
        video_url = data.get("resultObj", {}).get("videoURL")
        if not video_url:
            raise ValueError("videoURL/hdnea missing")

        # Extract hdnea token
        import re
        match = re.search(r"hdnea=([^&]+)", video_url)
        if not match:
            raise ValueError("hdnea token not found in videoURL")
        hdnea_token = match.group(1)

        # Save to as.txt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"# Fetched at {timestamp}\n")
            f.write(f"{hdnea_token}\n")

        print(f"✅ Token saved to {OUTPUT_FILE}")
        return hdnea_token

    except Exception as e:
        print(f"❌ Error fetching token: {e}")
        return None

if __name__ == "__main__":
    fetch_token()
