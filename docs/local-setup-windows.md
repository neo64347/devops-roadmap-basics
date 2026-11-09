# Optional: run the labs on your own Windows PC 🪟

The seminar uses **GitHub Codespaces**, so you don't need any of this on the day. Use this guide if you want to practise **at home on your own PC**.

> **Needs:** Windows 10 (2004+) or Windows 11, **admin rights**, virtualization enabled in BIOS, about 8 GB RAM.

## Which option?

| Option | Weight | Cost | Good for |
|---|---|---|---|
| **A. WSL2 + Docker Engine** ⭐ | Lightest | Free | Learning. Exactly like a Linux server |
| **B. Rancher Desktop** | Medium | Free, open source | People who prefer a GUI app |
| **C. Docker Desktop** | Heavier | Free for personal, education and small business; paid for larger companies | Most tutorials assume it |

> **What about Colima?** Colima is a great lightweight Docker runtime, but it only runs on **macOS and Linux**, not Windows. On Windows, option A is the closest equivalent.

---

## Option A: WSL2 + Docker Engine (recommended)

### 1. Install WSL2 with Ubuntu
Open **PowerShell as Administrator** and run:
```powershell
wsl --install -d Ubuntu
```
Restart when asked. After the restart, Ubuntu opens and asks you to create a Linux **username and password**.

### 2. Install Docker Engine inside Ubuntu
In the **Ubuntu** window:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```
Close Ubuntu and open it again (so the group change applies), then test:
```bash
docker run hello-world
docker compose version
```

> If `docker` says it can't connect: run `sudo service docker start`. On recent WSL versions you can make it start automatically by adding `[boot]` / `systemd=true` to `/etc/wsl.conf` and running `wsl --shutdown` in PowerShell.

### 3. Get the other tools
```bash
sudo apt update && sudo apt install -y git python3-pip python3-venv
```
For Terraform, follow <https://developer.hashicorp.com/terraform/install> (Linux → Ubuntu/Debian).

### 4. Get the labs
```bash
git clone https://github.com/YOUR-USERNAME/devops-roadmap-basics.git
cd devops-roadmap-basics
```
Open in VS Code with `code .` (install VS Code on Windows plus the **WSL** extension). Links like `localhost:8000` open in your Windows browser.

---

## Option B: Rancher Desktop
1. Download from <https://rancherdesktop.io> and install.
2. On first start choose **dockerd (moby)** as the container engine (so `docker` commands work) and you can **turn off Kubernetes** to save memory.
3. Open PowerShell or Windows Terminal: `docker run hello-world`.

---

## No admin rights?
Use the browser options. Nothing to install:
- **GitHub Codespaces**: what we use in the seminar.
- **Play with Docker**: <https://labs.play-with-docker.com> (free Docker Hub account, 4-hour sessions).
