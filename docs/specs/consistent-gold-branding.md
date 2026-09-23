# Consistent gold branding across the blog

## Goal

Make the header and appropriate accents on every post page use the same gold color as the redesigned homepage.

## References

* The attached homepage header screenshot shows the desired gold `norbix.dev` branding.
* The attached post page screenshot shows the current white `norbix.dev` branding.

Use the existing homepage CSS color value as the source of truth. Do not estimate a new gold from the screenshots.

## Requirements

1. Display `norbix.dev` in the same gold on the homepage, individual posts, post listings, About page, and other site pages.
2. Keep the header typography, spacing, navigation, theme toggle, and layout consistent across those pages.
3. Apply the existing gold accent to appropriate interactive details, such as active navigation indicators and hover or focus states, where this matches the homepage design.
4. Keep article titles, metadata, headings, code, and body text readable. Do not turn all post content gold.
5. Maintain readable colors in both dark and light themes, including keyboard focus states.
6. Use site-level CSS or layout overrides. Do not edit the PaperMod theme or its submodule. Reuse an existing shared color variable if one is available; otherwise define one shared gold value instead of duplicating color literals.

## Verification

Run `hugo --panicOnWarning`. Compare the homepage header with at least one post page and the `/posts/` listing at desktop and mobile widths. Check both theme modes and confirm the site title has the same intended gold color throughout.

Report the changed files. Do not deploy.
