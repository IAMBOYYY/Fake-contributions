import os
import subprocess
from datetime import datetime, timedelta

days_back = 365
commits_per_day = 4

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

start_date = datetime.now() - timedelta(days=days_back)

for i in range(days_back + 1):
    current_date = start_date + timedelta(days=i)
    formatted_date = current_date.strftime("%Y-%m-%dT12:00:00")

    for _ in range(commits_per_day):
        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = formatted_date
        env["GIT_AUTHOR_DATE"] = formatted_date
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "Fake commit"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    print(f"{GREEN}✅ Fake Green Square planted for: {formatted_date}")

print(f"{RED}🔥 All commits staged! Push to GitHub now!{RESET}")
