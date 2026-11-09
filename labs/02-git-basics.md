# Lab 2: Git & GitHub (60 min)

## 🎯 Goals
- Understand what Git and GitHub are
- Make a change, **commit** it and **push** it to GitHub
- Work on a **branch** and open a **pull request**

## 💡 The idea
- **Git** is a "save game" system for code. Every **commit** is a snapshot you can go back to.
- **GitHub** is a website that stores your Git repositories online so teams can share and review code.

```
 working folder ──git add──► staging area ──git commit──► local history ──git push──► GitHub
   (your edits)              (what goes in the           (snapshots on              (shared copy)
                              next snapshot)              your machine)
```

## 🛠️ Steps

### 1. Introduce yourself to Git (one time)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 2. Look at the history
```bash
git status        # what has changed?
git log --oneline # list of snapshots (commits)
```

### 3. Make a change
Create a new notes file:
```bash
echo "# My DevOps notes" > NOTES.md
echo "- Today I learned Git!" >> NOTES.md
git status        # NOTES.md shows as "untracked" (red)
```

### 4. Stage → commit → push
```bash
git add NOTES.md                     # put it in the staging area
git status                           # now green: ready to commit
git commit -m "Add my DevOps notes"  # take the snapshot with a message
git push                             # send it to GitHub
```
Refresh your repo page on GitHub. 🎉 `NOTES.md` is there.

> 💡 **Good commit messages** say *what* and *why*, for example: `Fix typo in greeting`, `Add health check endpoint`.

### 5. See what changed (diff)
```bash
echo "- Commits are snapshots" >> NOTES.md
git diff          # shows exactly what changed (+ added, - removed)
git commit -am "Add a note about commits"   # -a stages changed files, -m adds the message
git push
```

### 6. Branches & pull requests (how teams work)
A **branch** is a parallel copy where you can work safely without breaking `main`.
```bash
git switch -c my-first-branch       # create and move to a new branch
echo "- Branches keep main safe" >> NOTES.md
git commit -am "Add a note about branches"
git push -u origin my-first-branch
```
On GitHub you'll see a yellow banner: **Compare & pull request**. Click it → **Create pull request** → **Merge pull request** → **Confirm**.

Back in the terminal, update your local `main`:
```bash
git switch main
git pull
cat NOTES.md      # your branch's line is now in main
```

## ✅ Checkpoint
- [ ] `NOTES.md` is visible on GitHub with 3 notes
- [ ] You merged one pull request
- [ ] You can explain *add → commit → push* to your neighbour

## 🏋️ Mini challenge
Undo a mistake: add a silly line to `NOTES.md`, then throw the change away **before** committing:
```bash
git restore NOTES.md
```

## 🆘 Troubleshooting
| Problem | Fix |
|---|---|
| `Please tell me who you are` | Do step 1 |
| `nothing to commit` | You haven't changed anything, or forgot to save the file (<kbd>Ctrl</kbd>+<kbd>S</kbd>) |
| `rejected… fetch first` | Someone (maybe you, on GitHub) changed `main`. Run `git pull`, then `git push` again |
| Stuck in a strange editor after `git commit` | You forgot `-m`. Type `:wq` and press <kbd>Enter</kbd> to save and exit |

➡️ Next: [Lab 3: Docker basics](03-docker-basics.md)
