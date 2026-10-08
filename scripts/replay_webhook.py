"""Send a GitHub-shaped, signed workflow_run delivery for a real run to a Vecna goal webhook.

Usage:
  GOAL_HOOK_URL=http://localhost:8080/v1/hooks/goal/<token> GOAL_HOOK_SECRET=<hmac> \
    python3 scripts/replay_webhook.py [run_id]

With no run_id it sends the latest completed "PR" run on dev.
"""

import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request

REPO = "LALITH0110/ci-blame-sandbox"


def github(path):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def main():
    url, secret = os.environ["GOAL_HOOK_URL"], os.environ["GOAL_HOOK_SECRET"]
    if len(sys.argv) > 1:
        run = github(f"repos/{REPO}/actions/runs/{sys.argv[1]}")
    else:
        runs = github(f"repos/{REPO}/actions/runs?branch=dev&status=completed&per_page=20")["workflow_runs"]
        run = next(r for r in runs if r["name"] == "PR")
    payload = {
        "action": "completed",
        "workflow_run": run,
        "workflow": github(f"repos/{REPO}/actions/workflows/{run['workflow_id']}"),
        "repository": run["repository"],
        "sender": run["triggering_actor"],
        # The receiver drops a byte-identical body within the hour; this keeps each replay distinct.
        "replayed_at": int(time.time()),
    }
    body = json.dumps(payload).encode()
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "X-GitHub-Event": "workflow_run",
        "X-Hub-Signature-256": sig,
    })
    with urllib.request.urlopen(req) as resp:
        print(f"run {run['id']} ({run['conclusion']}, {run['head_sha'][:7]}) -> HTTP {resp.status}")


if __name__ == "__main__":
    main()
