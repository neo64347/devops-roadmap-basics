# Lab 5: CI/CD with GitHub Actions (60 min)

## 🎯 Goals
- Understand **CI** (Continuous Integration) and **CD** (Continuous Delivery/Deployment)
- Watch a pipeline run automatically on every push
- **Break** the build on purpose, see it go red ❌, then fix it ✅

## 💡 The idea
Imagine 10 developers changing the same app every day. Who checks that nothing broke? A **robot**.

- **CI:** every time code is pushed, automatically **test** it and **build** it.
- **CD:** if everything passes, automatically **release/deploy** it.

```
 git push ──► GitHub Actions ──► [ Run tests ] ──pass──► [ Build Docker image + smoke test ] ──► ✅
                                       │
                                     fail ──► ❌ stop, tell the developer
```

## 🛠️ Steps

### 1. Run the tests yourself first
```bash
cd app
pytest -v
cd ..
```
✅ `3 passed`. Look at `app/tests/test_app.py`: each `test_…` function checks one thing.

### 2. Read the pipeline
```bash
cat .github/workflows/ci.yml
```
- `on:` **when** it runs (every push to `main`, every pull request)
- `jobs:` **what** runs: `test`, then `build` (`needs: test` means build only runs if tests pass)
- `steps:` the commands, the same kind you typed in Lab 3 and in step 1 above

### 3. Trigger it
Your earlier pushes already ran it! On GitHub, open your repo → **Actions** tab. Click the latest run and watch the jobs and their logs.

Push something new to trigger a fresh run:
```bash
echo "- CI runs on every push" >> NOTES.md
git commit -am "Trigger CI"
git push
```
Go to **Actions** and watch it go 🟡 → ✅ (about 1 minute).

> 💡 **Or watch it from the VS Code terminal** with GitHub CLI:
> ```bash
> gh run watch      # pick the latest run; it updates live until it finishes
> gh run list       # recent runs with ✓ or X
> ```

### 4. Break it on purpose 🔨
Change the app's greeting in `app/app.py`:
```python
greeting = os.getenv("GREETING", "Hello, DevOps!")
```
to
```python
greeting = os.getenv("GREETING", "Hi there!")
```
Save, then:
```bash
git commit -am "Change greeting"
git push
```
In **Actions**, the **Run tests** job turns ❌ red. Click it and read the error: `test_home_says_hello` expected `Hello, DevOps!`. Notice that the **Build** job **never ran**. The pipeline protected us from shipping a change nobody checked.

### 5. Fix it
Either change the greeting back, **or** update the test to match the new behaviour in `app/tests/test_app.py`:
```python
    assert b"Hi there!" in response.data
```
Run `cd app && pytest -v && cd ..` locally first, then:
```bash
git commit -am "Update test for new greeting"
git push
```
✅ Back to green.

### 6. Add a status badge to your README
Edit `README.md` and add this line at the top (replace `YOUR-USERNAME`):
```markdown
![CI](https://github.com/YOUR-USERNAME/devops-roadmap-basics/actions/workflows/ci.yml/badge.svg)
```
Commit and push, then look at your repo's front page.

## ✅ Checkpoint
- [ ] You saw a green ✅ run and a red ❌ run
- [ ] You can explain why **Build** didn't run when tests failed
- [ ] Your README shows a CI badge

## 🏋️ Mini challenge
Add a 4th test that checks `/health` returns `status` equal to `"ok"` using a different style, or tests a page that doesn't exist returns `404`:
```python
def test_unknown_page_is_404():
    assert client().get("/nope").status_code == 404
```

## 💡 Where does CD come in?
In real projects, one more job would **push the image to a registry** and **deploy** it (to AWS, Azure, Kubernetes…). Same idea: just more steps in the YAML file.

## 🆘 Troubleshooting
| Problem | Fix |
|---|---|
| No runs in the Actions tab | Click **Actions** → enable workflows if GitHub asks ("I understand my workflows…") |
| `ModuleNotFoundError` when running pytest | Run it from inside the `app` folder: `cd app && pytest -v` |
| Push rejected | `git pull`, then `git push` |

➡️ Next: [Lab 6: Cloud, IaC & Monitoring](06-cloud-iac-monitoring.md)
