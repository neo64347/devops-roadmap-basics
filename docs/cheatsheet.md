# Cheat sheet 📋

## Linux terminal
| Command | What it does |
|---|---|
| `pwd` | Where am I? |
| `ls -la` | List all files with details |
| `cd folder` / `cd ..` / `cd ~` | Go into a folder / up one / home |
| `cat file` | Show a file |
| `mkdir name` | Create a folder |
| `echo "text" > file` | Write text to a file (`>>` appends) |
| `cp a b` / `mv a b` / `rm a` | Copy / move or rename / delete |
| `rm -r folder` | Delete a folder and its contents |
| `grep "word" file` | Find lines containing a word |
| `code file` | Open a file in the editor |
| <kbd>Tab</kbd> / <kbd>Ctrl</kbd>+<kbd>C</kbd> / <kbd>Ctrl</kbd>+<kbd>L</kbd> | Autocomplete / stop / clear screen |

## Git
| Command | What it does |
|---|---|
| `git status` | What changed? |
| `git add file` / `git add -A` | Stage one file / everything |
| `git commit -m "message"` | Save a snapshot |
| `git commit -am "message"` | Stage changed files and commit |
| `git push` / `git pull` | Send to / get from GitHub |
| `git log --oneline` | History |
| `git diff` | Show unstaged changes |
| `git switch -c name` | Create and switch to a branch |
| `git switch main` | Go back to main |
| `git restore file` | Throw away uncommitted changes to a file |

## GitHub CLI (`gh`)
| Command | What it does |
|---|---|
| `gh auth login` / `gh auth status` | Sign in (browser) / check who you are |
| `gh auth setup-git` | Let `git push` use your gh login |
| `gh repo create NAME --template OWNER/REPO --public --clone` | New repo from a template, downloaded |
| `gh repo clone OWNER/REPO` | Download a repo |
| `gh repo view --web` | Open the repo in the browser |
| `gh pr create --fill` | Open a pull request from your branch |
| `gh pr list` / `gh pr view --web` | List PRs / open one in the browser |
| `gh pr merge --merge --delete-branch` | Merge the PR and clean up the branch |
| `gh run list` / `gh run watch` | See GitHub Actions runs / follow one live |

## Docker
| Command | What it does |
|---|---|
| `docker run -d --name x -p 8080:80 image` | Run a container in the background |
| `docker ps` / `docker ps -a` | Running / all containers |
| `docker logs x` | Container output |
| `docker exec -it x sh` | Open a shell inside a container |
| `docker stop x` / `docker rm -f x` | Stop / force-remove |
| `docker build -t name:tag folder` | Build an image |
| `docker images` | List images |
| `docker system prune` | Clean up unused stuff |

## Docker Compose
| Command | What it does |
|---|---|
| `docker compose up -d --build` | Build and start everything |
| `docker compose ps` | Status |
| `docker compose logs -f web` | Follow logs for one service |
| `docker compose restart web` | Restart one service |
| `docker compose down` | Stop and remove everything |
| `docker compose --profile monitoring up -d` | Also start Prometheus + Grafana |

## Terraform
| Command | What it does |
|---|---|
| `terraform init` | Download providers (once per folder) |
| `terraform plan` | Preview changes |
| `terraform apply` | Make the changes |
| `terraform destroy` | Remove everything it created |

## Ports used today
| Port | What |
|---|---|
| 8000 | Our web app |
| 8080 | nginx (Lab 3, Terraform stretch) |
| 9090 | Prometheus |
| 3000 | Grafana |
