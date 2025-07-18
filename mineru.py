import requests
import time
import zipfile
import os
import json
import dotenv

dotenv.load_dotenv()

# === CONFIG ===
API_TOKEN = os.getenv("API_TOKEN")
LOCAL_FILE_PATH = "data/CV_của_Shiny-1.pdf"  # Replace with your local file
OUTPUT_DIR = "output"
OUTPUT_MD_FILE = "full.md"

# Record the start time
start_time = time.time()

# === Step 1: Get Upload URL ===
print("🔄 Requesting upload URL...")
upload_url = "https://mineru.net/api/v4/file-urls/batch"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}
file_name = os.path.basename(LOCAL_FILE_PATH)

payload = {
    "enable_formula": True,
    "language": "vi",
    "enable_table": True,
    "files": [
        {
            "name": file_name,
            "is_ocr": False,
            "data_id": "my_unique_id"
        }
    ]
}

res = requests.post(upload_url, headers=headers, json=payload)
res_json = res.json()

if res.status_code != 200 or res_json["code"] != 0:
    print("❌ Failed to get upload URL:", res.status_code, res.text)
    exit()

batch_id = res_json["data"]["batch_id"]
upload_link = res_json["data"]["file_urls"][0]

# === Step 2: Upload the File ===
print("⬆️ Uploading file...")
with open(LOCAL_FILE_PATH, "rb") as f:
    upload_res = requests.put(upload_link, data=f)
    if upload_res.status_code != 200:
        print("❌ Upload failed:", upload_res.status_code, upload_res.text)
        exit()

print(f"✅ Upload successful! Batch ID: {batch_id}")

# === Step 3: Poll for Results ===
print("🔍 Polling for parsing result...")

# Add a delay before starting the polling
time.sleep(2)  # Wait for 5 seconds before polling

result_url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"

while True:
    poll_res = requests.get(result_url, headers=headers)
    # Ensure the response is decoded in UTF-8
    response_content = poll_res.content.decode('utf-8')
    poll_json = json.loads(response_content)

    if poll_res.status_code != 200 or poll_json["code"] != 0:
        print("❌ Error polling result:", poll_res.status_code, poll_res.text)
        exit()

    all_done = True
    for doc in poll_json["data"]["extract_result"]:
        state = doc["state"]
        print(f"📄 {doc['file_name']} → {state}")

        if state == "done":
            zip_url = doc["full_zip_url"]
        elif state == "failed":
            print("❌ Parsing failed:", doc.get("err_msg"))
            exit()
        else:
            all_done = False

    if all_done:
        break
    time.sleep(3)

# === Step 4: Download and Extract `full.md` ===
print("📥 Downloading result ZIP...")
os.makedirs(OUTPUT_DIR, exist_ok=True)
zip_path = os.path.join(OUTPUT_DIR, "result.zip")
zip_content = requests.get(zip_url).content

with open(zip_path, "wb") as f:
    f.write(zip_content)

print(f"✅ ZIP downloaded to {zip_path}")

print("📦 Extracting full.md...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(OUTPUT_DIR)

md_path = os.path.join(OUTPUT_DIR, OUTPUT_MD_FILE)
if os.path.exists(md_path):
    print(f"✅ full.md extracted to {md_path}")
    # Remove or comment out the print statement for full.md content
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
else:
    print("❌ full.md not found in the extracted files.")

# Record the end time
end_time = time.time()

# Calculate and print the total time taken
total_time = end_time - start_time
print(f"⏱️ Total time for the cycle: {total_time:.2f} seconds")
