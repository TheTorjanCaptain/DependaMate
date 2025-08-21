# 🛡️ DependaMate

> **Analyze, Group, and Report Dependabot Alerts Like a Pro!**  
> Effortlessly fetch, group, and export all GitHub Dependabot alerts across multiple repositories in various formats — for visibility, auditing, and action.

---

## 🔍 What is DependaMate?

**DependaMate** is a powerful yet lightweight command-line tool that helps you fetch and organize GitHub Dependabot alerts from your repositories. Whether you're a security engineer, DevOps lead, or just someone trying to keep up with security best practices — DependaMate simplifies your workflow.

## ✨ Features

- ✅ Fetch Dependabot alerts from all your GitHub repositories.
- 📂 Automatically groups alerts per repository.
- 📁 Creates timestamped folders with all outputs neatly saved.
- 💾 Export results in multiple formats:
  - `JSON`
  - `CSV`
  - `Markdown`
- 🔐 Uses your GitHub Personal Access Token for secure API access.
- 💻 Cross-platform and beginner-friendly CLI.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/DependaMate.git
cd DependaMate
python3 Dependamate.py
```
Note: If you have MFA/SSO setup make sure to authorize it after creation of the Github token.
---

## 🛠 Requirements

- Python 3.7+
- A GitHub token with at least the following scopes:
  - repo
  - read:org

---

## 🔑 GitHub Token Setup

To use **DependaMate**, you'll need a **GitHub Personal Access Token (PAT)** with appropriate scopes or repository permissions depending on the type of token you use.

---

### ✅ Required Scopes (for **Classic Tokens**):
- `repo` – to read repository data and security alerts  
- `read:org` *(optional but recommended)* – if you're accessing organization-level private repositories

---

### ✅ Required Permissions (for **Fine-Grained Tokens**):
Assign the following **repository permissions** when generating a fine-grained token:

| Permission         | Access Level |
|--------------------|--------------|
| Dependabot alerts  | Read         |
| Contents           | Read         |
| Metadata *(optional)* | Read     |

---

### 🔐 Authorize Token for SSO (if applicable)

If you're part of a **GitHub organization that enforces SSO (Single Sign-On)**, just setting the scopes is **not enough**. You must **explicitly authorize the token** for access.

#### Steps:
1. Go to your [GitHub Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Find your newly created token
3. Click **"Enable SSO"**
4. Authorize it for the required organization(s)

Once you have the token ready and authorized, you can use it with DependaMate to fetch and manage Dependabot alerts securely and efficiently.

 
---

## 📈 Why Use DependaMate?

🔹 Save time checking multiple repos manually
🔹 Automate your audit or reporting pipeline
🔹 Easily track supply chain risks over time
🔹 Great for compliance and internal visibility


---

## 💡 Roadmap

- Export grouping by repo ✅ 

- Scheduler for periodic fetching

- Slack/Discord alerting

- PyPI packaging

---

## 🙌 Contributing

Pull requests and suggestions are welcome! Feel free to fork the repo and submit improvements.

---

## 🧠 License

MIT License © 2025

---

## 🔗 Connect

GitHub: https://github.com/yourusername/DependaMate

---

> **Disclaimer:**  
> This project, **DependaMate**, is an independent tool developed by [TheTorjanCaptain](https://github.com/TheTorjanCaptain).  
> It is **not affiliated with, endorsed by, or maintained by GitHub or the Dependabot team**.  
> It simply uses GitHub's public API to help developers manage their security alerts more easily.


