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
- [ ] Have the [backup plan](#backup-plan-play-with-docker) ready on a slide.
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

## 🛟 Backup plan: Play with Docker
If Codespaces is blocked or unavailable for some students:
1. Go to <https://labs.play-with-docker.com>, sign in with a free **Docker Hub** account, click **Start → + Add new instance**.
2. In the terminal:
   ```bash
   git clone https://github.com/YOUR-USERNAME/devops-roadmap-basics.git
   cd devops-roadmap-basics
   ```
3. Labs 1, 3 and 4 work fully (open ports using the port badges at the top). Lab 2 works for local commits (pushing needs a GitHub token, so skip the push steps). Lab 5 is done on github.com only (edit files in the browser with the ✏️ button; Actions still runs). Lab 6: monitoring works; Terraform isn't preinstalled, so demo it from your screen.

Sessions last 4 hours, so start a new instance after lunch.

## 🖥️ Your own demo machine
- **Mac:** Colima works well (`colima start --cpu 2 --memory 4`). Note macOS uses port 5000 for AirPlay, which is why the app uses **8000**.
- **Windows:** see [local setup](../docs/local-setup-windows.md) (WSL2 + Docker Engine).

## ✅ Answer key: common questions
- **"Is Docker a virtual machine?"** No. Containers share the host's kernel, so they're much lighter and faster to start.
- **"Why not just use Docker Desktop?"** It's fine and free for education, but needs admin rights and more RAM. Codespaces needs neither.
- **"Do companies really use GitHub Actions?"** Yes, alongside GitLab CI, Jenkins, Azure DevOps and others. The concepts transfer.
- **"Terraform vs Ansible?"** Terraform *creates* infrastructure. Ansible mostly *configures* what's already there.
