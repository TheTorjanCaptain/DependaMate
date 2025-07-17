import requests
import time
import datetime
import json
import os
import csv
from collections import defaultdict
from pathlib import Path

# === CONFIGURATION ===
TOOL_NAME = "DependaMate"
TOOL_URL = "https://github.com/TheTorjanCaptain/DependaMate"

def get_github_token():
    return input("Enter your GitHub Token: ").strip()

def get_org_name():
    return input("Enter GitHub Organization Name: ").strip()

def get_pr_state():
    while True:
        state = input("Enter PR state filter (open, closed, all): ").strip().lower()
        if state in ["open", "closed", "all"]:
            return state
        print("❌ Invalid input. Choose from 'open', 'closed', or 'all'.")

def print_banner():
    banner = r"""
_______                                                                               _______                                                                      
\  ___ `'.         __.....__   _________   _...._            __.....__        _..._   \  ___ `'.             __  __   ___                           __.....__      
 ' |--.\  \    .-''         '. \        |.'      '-.     .-''         '.    .'     '.  ' |--.\  \           |  |/  `.'   `.                     .-''         '.    
 | |    \  '  /     .-''"'-.  `.\        .'```'.    '.  /     .-''"'-.  `. .   .-.   . | |    \  '          |   .-.  .-.   '              .|   /     .-''"'-.  `.  
 | |     |  '/     /________\   \\      |       \     \/     /________\   \|  '   '  | | |     |  '    __   |  |  |  |  |  |    __      .' |_ /     /________\   \ 
 | |     |  ||                  | |     |        |    ||                  ||  |   |  | | |     |  | .:--.'. |  |  |  |  |  | .:--.'.  .'     ||                  | 
 | |     ' .'\    .-------------' |      \      /    . \    .-------------'|  |   |  | | |     ' .'/ |   \ ||  |  |  |  |  |/ |   \ |'--.  .-'\    .-------------' 
 | |___.' /'  \    '-.____...---. |     |\`'-.-'   .'   \    '-.____...---.|  |   |  | | |___.' /' `" __ | ||  |  |  |  |  |`" __ | |   |  |   \    '-.____...---. 
/_______.'/    `.             .'  |     | '-....-'`      `.             .' |  |   |  |/_______.'/   .'.''| ||__|  |__|  |__| .'.''| |   |  |    `.             .'  
\_______|/       `''-...... -'   .'     '.                 `''-...... -'   |  |   |  |\_______|/   / /   | |_               / /   | |_  |  '.'    `''-...... -'    
                               '-----------'                               |  |   |  |             \ \._,\ '/               \ \._,\ '/  |   /                      
                                                                           '--'   '--'              `--'  `"                 `--'  `"   `'-'                        

DependaMate — Analyze, Group, and Report Dependabot Alerts Like a Pro
🔗 https://github.com/TheTorjanCaptain/DependaMate
"""
    print(banner)

def get_date_input(prompt_text):
    while True:
        try:
            date_str = input(f"{prompt_text} (e.g., 2022-01-01): ").strip()
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.\n")

def daterange(start_date, end_date, step_months=1):
    date = start_date
    while date < end_date:
        next_month = date + datetime.timedelta(days=step_months * 31)
        yield (date, min(next_month, end_date))
        date = next_month

def fetch_dependabot_prs_between_dates(org, start_date, end_date, headers, state):
    all_prs = []
    page = 1
    per_page = 100
    base_url = "https://api.github.com/search/issues"

    created_range = f"{start_date.isoformat()}..{end_date.isoformat()}"

    # Build query with state filter (skip state if 'all')
    state_filter = f" state:{state}" if state != "all" else ""
    query = f"org:{org} is:pr author:dependabot[bot] created:{created_range}{state_filter}"

    print(f"\n🔍 Searching PRs from {created_range} with state '{state}'...")
    print(f"🔎 Query: {query}")

    while True:
        url = f"{base_url}?q={query}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 403:
            print(f"⏳ Rate limited. Sleeping 2 minutes...")
            time.sleep(120)
            continue
        elif response.status_code != 200:
            print(f"❌ Error fetching page {page}: {response.status_code} - {response.text}")
            break

        data = response.json()
        items = data.get("items", [])
        if not items:
            break

        all_prs.extend(items)
        print(f"✅ {len(items)} PRs from page {page}")
        page += 1

        if len(items) < per_page:
            break

        time.sleep(1)

    return all_prs

def group_by_repo(prs):
    grouped = defaultdict(list)
    for pr in prs:
        repo_url = pr.get("repository_url")
        if repo_url:
            repo_name = repo_url.split("/")[-1]
        else:
            repo_name = pr["html_url"].split("/")[4]
        grouped[repo_name].append(pr)
    print(f"Grouped into {len(grouped)} repositories")
    return grouped

def save_json(grouped_data, path):
    print(f"Saving JSON report to {path}")
    data_with_meta = {
        "_generated_by": f"{TOOL_NAME} - {TOOL_URL}",
        "timestamp": datetime.datetime.now().isoformat(),
        "data": grouped_data
    }
    with open(path, "w") as f:
        json.dump(data_with_meta, f, indent=2)

def save_csv(grouped_data, path):
    print(f"Saving CSV report to {path}")
    with open(path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([f"# Generated by {TOOL_NAME} - {TOOL_URL}"])
        writer.writerow(["Repository", "Title", "URL", "Created At"])
        for repo, prs in grouped_data.items():
            for pr in prs:
                writer.writerow([
                    repo,
                    pr["title"],
                    pr["html_url"],
                    pr["created_at"]
                ])

def save_markdown(grouped_data, path):
    print(f"Saving Markdown report to {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 📦 Dependabot PRs Grouped by Repository\n\n")
        f.write(f"_Generated by [{TOOL_NAME}]({TOOL_URL})_\n\n")
        for repo, prs in grouped_data.items():
            f.write(f"## 🗂 {repo} ({len(prs)} PRs)\n\n")
            for pr in prs:
                f.write(f"- [{pr['title']}]({pr['html_url']}) – _{pr['created_at']}_\n")
            f.write("\n")

def save_html(grouped_data, path):
    print(f"Saving HTML report to {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("<html><head><title>Dependabot PRs</title></head><body>")
        f.write(f"<h1>📦 Dependabot PRs Grouped by Repository</h1>")
        f.write(f"<p><em>Generated by <a href='{TOOL_URL}'>{TOOL_NAME}</a></em></p>")
        for repo, prs in grouped_data.items():
            f.write(f"<h2>{repo} ({len(prs)} PRs)</h2><ul>")
            for pr in prs:
                f.write(f'<li><a href="{pr["html_url"]}">{pr["title"]}</a> – <em>{pr["created_at"]}</em></li>')
            f.write("</ul>")
        f.write("</body></html>")

if __name__ == "__main__":
    print_banner()
    GITHUB_TOKEN = get_github_token()
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    ORG_NAME = get_org_name()
    PR_STATE = get_pr_state()
    START_DATE = get_date_input("Enter START DATE")
    END_DATE = get_date_input("Enter END DATE")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path(f"dependabot_reports_{timestamp}_{PR_STATE}")
    output_dir.mkdir(parents=True, exist_ok=True)

    final_prs = []
    for start, end in daterange(START_DATE, END_DATE, step_months=1):
        prs = fetch_dependabot_prs_between_dates(ORG_NAME, start, end, headers, PR_STATE)
        final_prs.extend(prs)
        time.sleep(1)

    if not final_prs:
        print("\n⚠️ No Dependabot PRs found with the given filters. Reports will not be generated.")
        exit(0)

    grouped = group_by_repo(final_prs)

    print(f"\n📁 Saving reports to folder: {output_dir}/")
    save_json(grouped, output_dir / f"dependabot_prs_{PR_STATE}.json")
    save_csv(grouped, output_dir / f"dependabot_prs_{PR_STATE}.csv")
    save_markdown(grouped, output_dir / f"dependabot_prs_{PR_STATE}.md")
    save_html(grouped, output_dir / f"dependabot_prs_{PR_STATE}.html")

    print(f"\n✅ Done! Total PRs fetched: {len(final_prs)}")
