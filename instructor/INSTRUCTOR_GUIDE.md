# Instructor guide 👩‍🏫

Audience: total beginners on Windows lab PCs, possibly **without admin rights**. Everything runs in **GitHub Codespaces** in the browser.

## 📅 Before the day

### 1–2 weeks before
- [ ] Ask students to **create a GitHub account** and **verify their email** (unverified accounts can't create Codespaces). Send them the repo link.
- [ ] Ask the venue: Chrome/Edge available? Can lab PCs reach `github.com`, `*.github.dev`, `*.app.github.dev`, `ghcr.io`, `mcr.microsoft.com`, `registry-1.docker.io`, `registry.terraform.io`? Corporate/school firewalls sometimes block these.
- [ ] Confirm this repo is a **template repository** (Settings → General → ✅ Template repository).

### The day before
- [ ] Dry run every lab yourself in a **fresh** Codespace from the template, timing each one.
- [ ] Pre-check Docker Hub pulls work from a Codespace (`docker pull nginx:alpine`).
- [ ] Test the [backup plan](#-backup-plan-killercoda-browser-playground) in a Killercoda playground (sign-in, `docker --version`, `bash scripts/start.sh`) and put the steps on a slide.
- [ ] Print or share the [cheat sheet](../docs/cheatsheet.md).

### On the day
- [ ] Start Lab 0 **first thing**. Codespace creation takes 1–2 minutes and is the most common blocker.
- [ ] Put the agenda, repo link and Wi-Fi details on the screen.
- [ ] Pair students up: a "driver" and a "navigator" who swap each lab.

## ⏱️ Timing & teaching notes

| Time | Lab | Teach (≤10 min) | Watch out for |
|---|---|---|---|
| 09:00 | 0 Setup | The DevOps loop; "automate the boring stuff" | Unverified GitHub emails; slow Codespace start |
| 09:45 | 1 Linux | Command anatomy, Tab completion, Ctrl+C | Paste shortcut (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd>); case-sensitive names |
| 10:45 | 2 Git | Draw *working → staging → commit → push* | `git commit` without `-m` opens an editor (`:wq`) |
| 11:45 | 3 Docker | Image = recipe, container = the cake 🎂 | Port pop-ups; leftover containers holding ports |
| 13:30 | 4 Compose | Services talk by name; data lives in Redis | Lab 3 container still on port 8000 → `docker rm -f my-app` |
| 14:15 | 5 CI/CD | Show the red ❌ run on the projector, then fix it together | First run may need "enable workflows" in the Actions tab |
| 15:30 | 6 Cloud/IaC/Monitoring | Pizza-as-a-service; plan/apply/destroy; "monitoring = smoke alarm" | Grafana "No data" until traffic is generated |
| 16:30 | 7 Wrap-up | Quiz, roadmap, **stop Codespaces** | |

**If you're running late**, these are safe to skip: Lab 2 step 6 (branches/PR), Lab 3 mini challenge, Lab 6 Part A (talk through it instead), the Terraform Docker stretch.

**Early finishers:** mini challenges at the end of each lab; [roadmap](../docs/roadmap.md) project ideas.

## 💰 Codespaces cost
Personal GitHub accounts include a **free monthly Codespaces allowance** (GitHub currently lists it in core-hours. Check <https://docs.github.com/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces> for current numbers). This repo requests a 2-core machine, so one seminar day uses only a small part of the allowance. Remind students to **stop** their Codespace at the end.

## 🛟 Backup plan: Killercoda browser playground
If Codespaces is blocked or unavailable for some students, use a free Linux playground in the browser.

> ⚠️ **Play with Docker (labs.play-with-docker.com) is shut down.** Its site says it is *"unavailable starting March 1, 2026"*. Don't put it on your slides.

1. Go to <https://killercoda.com/playgrounds/scenario/ubuntu> and sign in (free; GitHub or Google login works).
2. A terminal opens. Check Docker, and install it if the playground doesn't have it:
   ```bash
   docker --version || curl -fsSL https://get.docker.com | sh
   docker compose version
   ```
3. Get the labs (public repo, so no login needed to clone):
   ```bash
   git clone https://github.com/YOUR-USERNAME/devops-roadmap-basics.git
   cd devops-roadmap-basics
   bash scripts/start.sh
   ```
4. Open ports with Killercoda's **Traffic / Ports** menu (top right): type `8000`, `3000` or `9090`. `curl localhost:8000` works in the terminal.

**What works there:** Labs 1, 3, 4 and 6 (monitoring) fully. Lab 2 works for local commits; to push, students need `gh auth login` (install `gh` as in the [Windows guide, step 7](../docs/local-setup-windows.md#7-install-github-cli-and-sign-in)), or they skip the push steps. Lab 5 can be done on github.com only (edit files in the browser with the ✏️ button; Actions still runs). Terraform isn't preinstalled, so demo Lab 6 Part A from your screen.

**Limits:** free sessions are time-limited (around 1 hour at the time of writing) and are wiped when they end. Check the current limit on the site the day before. Students should **push their work before the timer ends**, then start a new playground and `git clone` again.

**Second option:** [iximiuz Labs Docker playground](https://labs.iximiuz.com/playgrounds/docker): a Linux server with Docker preinstalled, free account, also time-limited.

**Last resort:** pair students without a working environment with a neighbour who has one, and swap the driver role each lab.

## 🖥️ Your own demo machine
- **Mac:** Colima works well (`colima start --cpu 2 --memory 4`). Note macOS uses port 5000 for AirPlay, which is why the app uses **8000**.
- **Windows:** see [local setup](../docs/local-setup-windows.md) (WSL2 + Docker Engine).
- **Sharing your VS Code extensions:** on your Mac run `scripts/vscode/export-from-mac.sh`. It reads your installed extensions, keeps only the ones with a Windows build on the Marketplace, skips AI assistants and account-based tools (Claude, Cursor, OpenAI, Copilot, Codacy), and rewrites `scripts/vscode/extensions.txt`. Review the diff, commit and push. Students install them with step 12 of the Windows guide.

## ✅ Answer key: common questions
- **"Is Docker a virtual machine?"** No. Containers share the host's kernel, so they're much lighter and faster to start.
- **"Why not just use Docker Desktop?"** It's fine and free for education, but needs admin rights and more RAM. Codespaces needs neither.
- **"Do companies really use GitHub Actions?"** Yes, alongside GitLab CI, Jenkins, Azure DevOps and others. The concepts transfer.
- **"Terraform vs Ansible?"** Terraform *creates* infrastructure. Ansible mostly *configures* what's already there.
