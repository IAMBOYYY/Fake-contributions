import os
import subprocess
from datetime import datetime, timedelta

# ---- CONFIG ----
commits_per_day = 12   # HIGHER = DARKER squares (keep same every run)
START_DATE = None      # None = auto: day AFTER your last commit. Or set "2026-09-15"
END_DATE = None        # None = today

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def get_last_commit_date():
    r = subprocess.run(
        ["git", "log", "-1", "--format=%aI"],
        capture_output=True, text=True
    )
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return datetime.fromisoformat(r.stdout.strip())

# Pick start date
if START_DATE:
    start = datetime.fromisoformat(START_DATE)
else:
    last = get_last_commit_date()
    if last:
        start = last + timedelta(days=1)   # begin right where the graph went gray
    else:
        start = datetime.now() - timedelta(days=365)

end = datetime.fromisoformat(END_DATE) if END_DATE else datetime.now()
total_days = (end.date() - start.date()).days

if total_days < 0:
    print(f"{RED}Nothing to fill — start date is in the future.{RESET}")
else:
    print(f"{GREEN}Filling {total_days + 1} day(s) with {commits_per_day} commits each...{RESET}")
    for i in range(total_days + 1):
        current_date = start + timedelta(days=i)
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
        print(f"{GREEN}✅ Filled: {formatted_date[:10]}{RESET}")

    print(f"{RED}🔥 Done! Push with: git push{RESET}")
        
