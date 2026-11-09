# Run the labs on your own Windows PC 🪟

The seminar uses **GitHub Codespaces**, so you don't need any of this on the day. Use this guide to practise **on your own PC**, or if your lab PCs allow installing software.

You'll set up **WSL2 + Ubuntu + Docker Engine**: the lightest, free way to run Docker on Windows (the Windows equivalent of Colima on a Mac). All lab commands then work exactly as written.

---

## 0. Requirements (check first)

| Requirement | How to check |
|---|---|
| Windows 10 version 22H2 or Windows 11 | <kbd>Win</kbd>+<kbd>R</kbd> → type `winver` → Enter |
| **Administrator rights** | You can "Run as administrator" |
| **Virtualization enabled** | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Esc</kbd> → **Performance** → **CPU** → "Virtualization: **Enabled**". If Disabled, turn on *Intel VT-x* / *AMD-V (SVM)* in the BIOS/UEFI settings |
| 8 GB RAM (16 GB recommended for the monitoring lab) | Task Manager → Performance → Memory |
| 20 GB free disk space | File Explorer → This PC |
| Internet access | — |

### What you'll install

| # | Tool | Where | Why |
|---|---|---|---|
| 1 | WSL2 + Ubuntu | Windows | A real Linux system inside Windows |
| 2 | Docker Engine + Compose | Ubuntu | Containers (Labs 3, 4, 6) |
| 3 | Git, Python 3, pip, venv | Ubuntu | Labs 1, 2, 5 |
| 4 | Terraform | Ubuntu | Lab 6 |
| 5 | VS Code + WSL extension | Windows | Editor and terminal |
| 6 | GitHub CLI (`gh`) | Ubuntu | Sign in to GitHub, push, create repos and pull requests from the terminal |

⏱️ About **30–45 minutes**, mostly downloads.

---

## 1. Install WSL2 and Ubuntu
1. Click **Start**, type `PowerShell`, right-click **Windows PowerShell** → **Run as administrator**.
2. Run:
   ```powershell
   wsl --install -d Ubuntu
   ```
   > **Red error about `Microsoft.PowerShell_profile.ps1 cannot be loaded because running scripts is disabled`?** It's harmless. You can still type commands. To stop it appearing, run this once, answer **Y**, then reopen PowerShell:
   > ```powershell
   > Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   > ```
   > This lets your own local scripts run (downloaded scripts still need a signature) and only affects your user account.
3. **Restart** the PC when asked.
4. After restart an **Ubuntu** window opens (if not: Start → Ubuntu). Wait for it to finish, then create a Linux **username** and **password** (the password is invisible while typing, which is normal. Remember it, `sudo` asks for it).

✅ Check, in PowerShell:
```powershell
wsl -l -v
```
Ubuntu should show **VERSION 2**. If it shows 1: `wsl --set-version Ubuntu 2`.

> From now on, every command goes in the **Ubuntu** terminal, unless it says PowerShell.

## 2. Update Ubuntu
```bash
sudo apt update && sudo apt upgrade -y
```

## 3. Install Docker Engine (no Docker Desktop needed)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```
**Close the Ubuntu window and open it again** (so you can use `docker` without `sudo`). Then:
```bash
docker run hello-world
docker compose version
```
✅ You see "Hello from Docker!" and a Compose version.

> **`Cannot connect to the Docker daemon`?** Start it with `sudo service docker start`. To make it start automatically, check that systemd is on: `cat /etc/wsl.conf` should contain
> ```
> [boot]
> systemd=true
> ```
> If not, add those two lines (`sudo nano /etc/wsl.conf`), then in **PowerShell** run `wsl --shutdown` and reopen Ubuntu.

## 4. Install Git, Python and tools
```bash
sudo apt install -y git curl python3 python3-pip python3-venv
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 5. Install Terraform
```bash
sudo apt install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
```

## 6. Install VS Code and open it in Ubuntu
1. Download and install VS Code on **Windows** from <https://code.visualstudio.com>.
2. Open VS Code → Extensions (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>) → install **WSL** (by Microsoft).
3. In the **Ubuntu** window, run:
   ```bash
   cd ~
   code .
   ```
   The first time, VS Code installs a small server inside Ubuntu (about 1 minute).
4. Check the **bottom-left corner** of VS Code. It must say **WSL: Ubuntu**. If not: press <kbd>F1</kbd> → type `WSL: Connect to WSL` → Enter.
5. Open the built-in terminal: <kbd>Ctrl</kbd>+<kbd>`</kbd> (the key above Tab), or **Terminal → New Terminal**.

> From now on, type every command in the **VS Code terminal**. It's the same Ubuntu terminal, right next to your files.

## 7. Install GitHub CLI and sign in
The **GitHub CLI** (`gh`) lets you sign in to GitHub once and then push, create repos and open pull requests from the terminal. No passwords or tokens to copy.

In the VS Code terminal:
```bash
sudo mkdir -p -m 755 /etc/apt/keyrings
wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install -y gh
gh --version
```

Sign in:
```bash
gh auth login
```
Answer the questions with the arrow keys and <kbd>Enter</kbd>:

| Question | Choose |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| Preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate? | **Login with a web browser** |

`gh` shows a **one-time code** like `ABCD-1234`. Copy it, press <kbd>Enter</kbd>, and a browser page opens (if it doesn't, <kbd>Ctrl</kbd>+click the `https://github.com/login/device` link). Paste the code → **Continue** → **Authorize GitHub CLI**.

✅ Check:
```bash
gh auth status
```
It shows `✓ Logged in to github.com account YOUR-USERNAME`. Git now uses this login for `git push`, so you won't be asked for a password.

> Never paste a GitHub password or token into chat or a file. `gh auth login` stores the login safely for you. To sign out: `gh auth logout`.

## 8. Get the labs
Create **your own copy** of the labs from the template and download it, in one command (still in the VS Code terminal):
```bash
cd ~
gh repo create devops-roadmap-basics --template neo64347/devops-roadmap-basics --public --clone
cd devops-roadmap-basics
code -r .
```
`code -r .` reopens VS Code in the project folder. Open the terminal again with <kbd>Ctrl</kbd>+<kbd>`</kbd>.

> Prefer the website? On GitHub click **Use this template → Create a new repository**, then run `gh repo clone YOUR-USERNAME/devops-roadmap-basics`.

> Keep your projects **inside Ubuntu** (`~/...`), not under `/mnt/c/...`. It's much faster.

## 9. Set up Python for the labs (one time)
Ubuntu doesn't allow `pip install` system-wide, so create a **virtual environment**:
```bash
cd ~/devops-roadmap-basics
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt -r app/requirements-dev.txt
```
Your prompt now starts with `(.venv)`. **Each time you open a new terminal**, run `source .venv/bin/activate` before Lab 5's `pytest`.

## 10. ✅ Final check
```bash
git --version && gh --version && docker --version && docker compose version && python3 --version && terraform --version
gh auth status
docker compose up -d --build && sleep 5 && curl localhost:8000 && docker compose down
```
✅ The last command prints `Hello from Docker Compose! You are visitor #1.`

Links like <http://localhost:8000>, <http://localhost:3000> (Grafana) and <http://localhost:9090> (Prometheus) open in your normal **Windows** browser.

You're ready. Start at [Lab 1](../labs/01-linux-basics.md) (skip the Codespaces part of Lab 0).

---

## 🆘 Troubleshooting

| Problem | Fix |
|---|---|
| `wsl --install` says virtualization is not enabled | Enable Intel VT-x / AMD-V in BIOS. Also check **Turn Windows features on or off** → ✅ *Virtual Machine Platform* and ✅ *Windows Subsystem for Linux* |
| PowerShell: `...profile.ps1 cannot be loaded because running scripts is disabled` | Harmless, keep going. To fix it: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer **Y**, reopen PowerShell |
| Error `0x80370102` | Same as above: virtualization is off in BIOS |
| `permission denied ... docker.sock` | You skipped reopening Ubuntu after `usermod`. Close and reopen it (or run `newgrp docker`) |
| `error: externally-managed-environment` on pip | Use the virtual environment (step 9) |
| `code: command not found` in Ubuntu | Install the VS Code **WSL** extension, close and reopen Ubuntu, try `code .` again |
| VS Code bottom-left doesn't say **WSL: Ubuntu** | <kbd>F1</kbd> → `WSL: Connect to WSL`. Commands in a plain Windows terminal won't find `docker` or `gh` |
| `gh auth login` doesn't open a browser | <kbd>Ctrl</kbd>+click the `https://github.com/login/device` link, or open it in your browser and paste the code |
| `git push` asks for a username/password | Run `gh auth setup-git` (or `gh auth login` again and answer **Yes** to "Authenticate Git") |
| `gh: command not found` | Rerun step 7, or open a new terminal |
| `localhost:8000` doesn't open in the Windows browser | Run `wsl --shutdown` in PowerShell, reopen Ubuntu, start the containers again |
| WSL uses too much memory | Create `C:\Users\<you>\.wslconfig` with `[wsl2]` and `memory=4GB` on the next line, then `wsl --shutdown` |
| Ports 8000/3000 "already in use" | Another program uses them. Stop it, or change the left-hand port in `compose.yaml` (e.g. `"8001:8000"`) |

---

## Alternatives

| Option | When to use it |
|---|---|
| **Rancher Desktop** (<https://rancherdesktop.io>, free) | You prefer a GUI app. On first start choose **dockerd (moby)** and turn **off** Kubernetes to save memory. It uses WSL2 too, so step 0 still applies |
| **Docker Desktop** | Most tutorials assume it. Free for personal/education/small business, heavier, needs admin |
| **No admin rights** | Use the browser: **GitHub Codespaces** (what the seminar uses) or **Play with Docker** (<https://labs.play-with-docker.com>) |

> **Why not Colima?** Colima only runs on **macOS and Linux**. WSL2 + Docker Engine is the Windows equivalent.
