Update the homepage of this Hugo blog to closely match the reference mockup I provide. The project uses Hugo v0.145.0 and the PaperMod theme. First inspect the repository, including `hugo.toml`, existing layouts, CSS, the PaperMod version, and actual posts. Then implement and verify the changes.

**Visual target**

Keep the dark background and my existing gold Spartan avatar. Create a spacious, editorial homepage with restrained gold accents:

* A compact header with `norbix.dev` and the existing navigation.
* A centered hero with the avatar, “Norbert Jakubczak”, and “SOFTWARE ENGINEER · TECHNOLOGY PARTNER”.
* A prominent headline: “Think independently. Build deliberately.” Highlight “independently” and “deliberately” in gold.
* Supporting text: “Engineering notes on software systems, architecture, and the decisions behind them.”
* Three understated links: “Read the notes” → `/posts/`, “About me” → `/about/`, and “Work with me” → the existing work/contact page. Find and use its real URL; do not create a dead link.
* A small, letter-spaced topic line: “DISTRIBUTED SYSTEMS · GO · PYTHON · TYPESCRIPT · AWS · KUBERNETES”.
* A “Latest posts” section below the hero with two cards populated automatically from the two most recent published posts. Show each post’s actual title, date, summary where available, and relevant tags. Link the whole card or its title to the post. Include “View all posts” → `/posts/`.

The mockup contains invented post titles and dates. Do not copy them into the site. Use my real content.

**Implementation**

Use site-level Hugo overrides and CSS; do not edit files inside `themes/PaperMod` or the theme submodule. Inspect how this installed PaperMod version loads custom CSS and follow that mechanism. Replace the current PaperMod profile layout on the homepage as needed to achieve the visual hierarchy. Avoid relying on HTML embedded in the `profileMode.subtitle` TOML string for the finished layout.

Preserve the existing post pages, navigation destinations, dark/light theme toggle, RSS, metadata, comments, and responsive behavior. Keep the existing avatar image. Make the hero, links, and post cards work well on desktop and mobile, with accessible focus states and readable contrast. Do not add a large stock image, external font dependency, or new JavaScript framework.

Keep copy and URLs in appropriate Hugo configuration where practical. Remove obsolete commented homepage markup from `hugo.toml`. Check that site-wide parameters such as `author`, `description`, and `ShowReadingTime` are under `[params]`, rather than accidentally scoped under `[params.homeInfoParams]`.

**Verification**

Run `hugo --panicOnWarning` using the available Hugo version. Inspect the generated homepage or local preview at desktop and mobile widths. Confirm that all three hero links and both post links resolve, that the post cards show real content, and that the existing post layout remains intact. Report which files changed and any intentional differences from the mockup. Do not publish or deploy the site.
