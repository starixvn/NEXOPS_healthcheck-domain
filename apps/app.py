import requests
from concurrent.futures import ThreadPoolExecutor
import os
import time

EXPECTED = "KLPROD"
URL_PATH = "/cluster-name"
TIMEOUT = 5
THREADS = 200

#curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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


def check(domain, system, retry=3, delay=1):
    for attemp in range(retry):
      try:
          r = requests.get(f"https://{domain}{URL_PATH}", timeout=TIMEOUT)
          body = r.text.strip()
          if r.status_code == 200 and body == EXPECTED:
              print(f"[{system}] ✅ {domain} OK")
          else:
              print(f"[{system}] ❌ {domain} FAIL - status={r.status_code}")
              return domain
      except Exception as e:
          if attemp < retry:
            time.sleep(delay)
          else:
            print(f"[{system}] ❌ {domain} ERROR: {e}")            
            return domain



import requests
import json

# SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")  # export biến này vào CronJob
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"  # export biến này vào CronJob

def send_slack_message(message):
    if SLACK_WEBHOOK:
        try:
            requests.post(SLACK_WEBHOOK, json={"text": message})
        except Exception as e:
            print(f"[Slack] ❌ Failed to send message: {e}")





def run_for_file(file_path):
    system_name = os.path.basename(os.path.dirname(file_path))  # e.g. 'was'

    with open(file_path) as f:
        domains = list(set(line.strip() for line in f if line.strip()))

    total = len(domains)

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        failed = list(filter(None, executor.map(lambda d: check(d, system_name), domains)))

    if failed:
        with open(f"failed_{system_name}.log", "w") as f:
            f.write("\n".join(failed))

    # Slack message format
    message = f"✅ Completed domain health check for *system `{system_name}`*\n" \
              f"Total domains checked: {total}\n"

    if failed:
        message += f"❌ Failed: {len(failed)}\n" + "\n- " + "\n- ".join(failed)
    else:
        message += "✅ All domains are correct mapping 🎉"

    send_slack_message(message)


####
def main():
    folder = "domains"
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, folder)
                system_name = rel_path.replace("/", "_").replace(".txt", "")
                run_for_file(file_path)
                
if __name__ == "__main__":
    main()
