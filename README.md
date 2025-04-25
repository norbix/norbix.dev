# SDLC Playbook

This repository contains the source code and content behind [https://norbix.dev](https://norbix.dev) — a personal knowledge base and technical playbook by Norbert Jakubczak (Mr. Norbix), focused on Software Development Lifecycle (SDLC), DevOps, and engineering practices. Built with [Hugo](https://gohugo.io/) and deployed via GitHub Pages.

![banner](static/images/banner.jpg)

---

## 📊 Analytics

Visitor analytics are powered by [GoatCounter](https://www.goatcounter.com) — a lightweight, privacy-friendly alternative to Google Analytics.

You can explore page view trends and traffic stats publicly at:  
👉 **[https://norbix.goatcounter.com](https://norbix.goatcounter.com)**

---

## 📨 Subscribers

Email subscriptions are handled via [Buttondown](https://buttondown.email) — a lightweight, privacy-first newsletter engine built for indie developers.

Visitors can subscribe to receive new blog posts and updates directly to their inbox.

🔔 Manage subscribers and view the list here (owner-only):  
👉 **[https://buttondown.com/subscribers](https://buttondown.com/subscribers)**

The subscription form is embedded directly on individual blog posts using a custom Hugo partial.

---

## 🔐 How to get your Google Site Verification token

1. Go to Google Search Console.

2. Add your domain (e.g. norbix.dev) under the Domain property.

3. Copy the TXT record that looks like this:
  
  ```text
  google-site-verification=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

4. Add it to your DNS provider (e.g. Cloudflare or Porkbun) as a TXT record with:

- Host: @ (or leave empty)

- Value: your full token

5. Save and wait a few minutes, then click Verify in Search Console.

You can check propagation using:

```text
dig TXT norbix.dev +short
```

---

## 🔍 Google Search Console

To improve search visibility and SEO performance, norbix.dev is connected to Google Search Console.

This allows tracking of:

- Indexed pages

- Search queries bringing traffic

- Click-through rates from Google results

- Crawling and indexing issues

The site submits its automatically generated sitemap.xml to help Google index new blog posts more quickly.

💡 Verification is done via a DNS TXT record or HTML file (configurable via your domain provider or Hugo's `static/` directory).

🔗 Google Search Console: [https://search.google.com/search-console](https://search.google.com/search-console)

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

The domain `norbix.dev` is registered through [Porkbun](https://porkbun.com), and DNS is managed via [Cloudflare](https://cloudflare.com).  
GitHub Pages handles hosting, while the domain itself points to GitHub's IPs using A and CNAME records.

Domain configuration is defined via `static/CNAME`, which contains: `norbix.dev`.

#### 🔍 DNS Verification

To verify DNS records (such as the `google-site-verification` TXT record), you can use:

```text
dig TXT norbix.dev +short
````

This is especially useful to confirm Google Search Console verification is active and propagated.

#### 🔍 WHOIS Lookup

To check in WHOIS, you can use [https://www.whois.com/whois/norbix.dev](https://www.whois.com/whois/norbix.dev)

#### 🔍 Check DNS Propagation

Check [https://dnschecker.org/#TXT/norbix.dev)(https://dnschecker.org/#TXT/norbix.dev) to verify if `TXT` record is propagated across different DNS servers.

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

## 🔍 Uptime Monitoring

The uptime and availability of [norbix.dev](https://norbix.dev) are monitored using [UptimeRobot](https://uptimerobot.com/) to ensure the site is consistently accessible.

📈 You can view real-time uptime stats here:  
👉 **[https://stats.uptimerobot.com/4eFg4Cd2zt](https://stats.uptimerobot.com/4eFg4Cd2zt)**

Alerts are configured to notify if the site becomes unreachable, helping keep the platform reliable and always available.

---

## 🤝 Contributing

This is a personal site, but you're welcome to open issues or PRs if you spot something broken or want to suggest an improvement.

---

## 📜 License

MIT — see `LICENSE` for details.
