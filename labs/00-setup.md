# Lab 0: Setup & What is DevOps? (45 min)

## 🎯 Goals
- Understand what DevOps is in one sentence
- Open your own Codespace, the computer you'll use all day

## 💡 What is DevOps?

> **DevOps is how teams deliver software quickly *and* safely, by automating the boring, error-prone steps between "I wrote some code" and "users are happily using it".**

The DevOps loop:

```
   PLAN → CODE → BUILD → TEST → RELEASE → DEPLOY → OPERATE → MONITOR
     ▲                                                          │
     └────────────────── learn & improve ◄──────────────────────┘
```

| Today's topic | Part of the loop | Why it matters |
|---|---|---|
| Linux terminal | Everywhere | Most servers run Linux and are controlled by typing commands |
| Git & GitHub | Code | Save every version of your work and collaborate safely |
| Docker | Build, Release | "It works on my machine" becomes "it works everywhere" |
| CI/CD | Test, Release, Deploy | Robots test and build your code on every change |
| Infrastructure as Code | Deploy, Operate | Create servers from files, not by clicking around |
| Monitoring | Monitor | Know when something breaks before your users tell you |

## 🛠️ Steps

### 1. Make your own copy of this repo
1. Sign in to GitHub.
2. Open the seminar repository and click the green **Use this template** button → **Create a new repository**.
3. **Repository name:** `devops-roadmap-basics`. Keep it **Public**. Click **Create repository**.

> Why your own copy? You'll push changes and run pipelines, and you need to own the repo to do that.

### 2. Open a Codespace
1. In **your** new repo, click **Code** → **Codespaces** tab → **Create codespace on main**.
2. A VS Code editor opens in your browser. The first start takes **1–2 minutes** while it installs tools.
3. When you see a terminal at the bottom with a prompt like `@yourname ➜ /workspaces/devops-roadmap-basics (main) $`, you're ready.

> No terminal? Press <kbd>Ctrl</kbd> + <kbd>`</kbd> (the key above Tab), or use the menu **☰ → Terminal → New Terminal**.

### 3. Check your tools
Copy each command, paste it into the terminal (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd> or right-click → Paste) and press <kbd>Enter</kbd>:

```bash
git --version
docker --version
python --version
terraform --version
```

✅ **Checkpoint:** each command prints a version number, for example `Docker version 2x.x.x`.

## 🆘 Troubleshooting

| Problem | Fix |
|---|---|
| No **Use this template** button | Make sure you're signed in to GitHub |
| Codespace stuck on "Setting up" for 5+ minutes | Refresh the page. Still stuck? Go to <https://github.com/codespaces>, delete it, and create a new one |
| `docker: command not found` | Wait a minute (it may still be installing), then open a new terminal |
| Codespaces not available for your account | Ask the instructor for the backup: a free [Killercoda](https://killercoda.com/playgrounds/scenario/ubuntu) Linux playground in the browser ([steps](../instructor/INSTRUCTOR_GUIDE.md#-backup-plan-killercoda-browser-playground)) |

## 💰 Is Codespaces free?
Personal GitHub accounts get a **free monthly allowance** of Codespaces hours, far more than one day needs. To save hours, **stop** your Codespace when you finish: <https://github.com/codespaces> → **⋯** → **Stop codespace**. It also stops by itself after 30 minutes of inactivity.

➡️ Next: [Lab 1: Linux terminal basics](01-linux-basics.md)
