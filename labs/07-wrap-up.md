# Lab 7: Wrap-up & your roadmap (30 min)

## 🎉 What you did today
You took one app through the full DevOps loop:

| ✅ | Skill | Tool you used |
|---|---|---|
| ✅ | Controlled a Linux machine from the terminal | bash |
| ✅ | Tracked changes and collaborated with branches and pull requests | Git, GitHub |
| ✅ | Packaged an app so it runs the same everywhere | Docker |
| ✅ | Ran a multi-container app with one command | Docker Compose |
| 💬 | Understood VMs vs containers, Kubernetes, monolith vs microservices, web app vs API | Discussion |
| ✅ | Automated testing and building on every push | GitHub Actions |
| ✅ | Created and destroyed infrastructure from code | Terraform |
| ✅ | Watched an app live and caught an outage | Prometheus, Grafana |

That is the foundation of every DevOps job. 🙌

## 🧠 Quick quiz (discuss with your neighbour)
1. What's the difference between an **image** and a **container**?
2. Why did the **Build** job not run when a test failed?
3. Why is it better to create servers with **Terraform** than by clicking in a web console?
4. What does `git push` do?
5. Your app is down at 2 a.m. What tells you before users complain?
6. Name one difference between a **VM** and a **container**, and one job **Kubernetes** does that Docker Compose doesn't.
7. A 3-person start-up: **monolith** or **microservices**? Is `/health` part of a **web app** or an **API**?

<details>
<summary>Answers</summary>

1. An image is the template. A container is a running copy of it.
2. `needs: test`: the pipeline stops early so broken code isn't shipped.
3. It's repeatable, reviewable in Git, and documents itself.
4. Sends your local commits to GitHub.
5. Monitoring and alerting (e.g. Prometheus + Grafana).
6. A VM has its own OS (GBs, minutes to boot); a container shares the host kernel (MBs, seconds). Kubernetes runs containers across many machines and self-heals or scales them.
7. Usually a monolith (simpler, faster to start). `/health` is an API: it returns JSON for machines.
</details>

## 🗺️ What to learn next
See **[docs/roadmap.md](../docs/roadmap.md)** for a step-by-step path, free resources and project ideas.

## 🧹 Before you leave
1. Commit and push anything you want to keep: `git add -A && git commit -m "End of seminar" && git push`
2. **Stop your Codespace** to save your free hours: <https://github.com/codespaces> → **⋯** → **Stop codespace**.
3. Your repository stays on GitHub. It's the start of your DevOps portfolio! ⭐

## 🙏 Feedback
Tell the instructor one thing you liked and one thing to improve. Thank you!
