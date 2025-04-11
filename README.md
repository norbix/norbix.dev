# SDLC Playbook

This repository contains the source code and content behind [https://norbix.dev](https://norbix.dev) — a personal knowledge base and technical playbook by Norbert Jakubczak (Mr. Norbix), focused on Software Development Lifecycle (SDLC), DevOps, and engineering practices. Built with [Hugo](https://gohugo.io/) and deployed via GitHub Pages.

## 📊 Analytics

Visitor analytics are powered by [GoatCounter](https://www.goatcounter.com) — a lightweight, privacy-friendly alternative to Google Analytics.

You can explore page view trends and traffic stats publicly at:  
👉 **[https://norbix.goatcounter.com](https://norbix.goatcounter.com)**

## Table of Contents
- [🛠️ Tech Stack](#-tech-stack)
- [🚀 Deployment](#-deployment)
  - [🔗 Live URL](#-live-url)
  - [🧾 Domain](#-domain)
- [🧼 Local Development](#-local-development)
- [🛠 Updating Content](#-updating-content)
- [🔄 Maintenance & Updates](#-maintenance--updates)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🛠️ Tech Stack

- **Hugo** — Static Site Generator
- **GitHub Pages** — Hosting
- **Custom Domain** — `norbix.dev` (configured via `static/CNAME`)
- **Theme** — [Your Hugo theme name] (see `themes/` directory)

---

## 🚀 Deployment

The site is automatically deployed to GitHub Pages from the `main` branch using GitHub Actions.

### 🔗 Live URL
👉 [https://norbix.dev](https://norbix.dev)

### 🧾 Domain
Custom domain is set via `static/CNAME` containing `norbix.dev`

---

## 🧼 Local Development

```text
git clone https://github.com/norbix/norbix.dev.git
cd norbix.dev
hugo server -D
```

Then open your browser at: http://localhost:1313

---

## 🛠 Updating Content

All blog posts and pages live in the content/ directory.

To create a new blog post:

```text
hugo new blog/my-new-post.md
```

---

## 🔄 Maintenance & Updates

- Content updates: via commits to content/ directory

- Theme updates: managed via submodule in themes/ (see .gitmodules)

- Build config: defined in hugo.toml

- Domain config: via static/CNAME

- Static assets: (e.g. images, CSS overrides) go in static/

---

## 🤝 Contributing

This is a personal site, but you're welcome to open issues or PRs if you spot something broken or want to suggest an improvement.

---

## 📜 License

MIT — see `LICENSE` for details.

