# Published Essays – Workflow & Guidelines

This folder contains the published, shareable versions of exgetical articles—both close readings of single passages and theme essays. The goal is to keep the process simple, consistent, and maintainable so new essays can be added quickly without reinventing layout or structure each time.

## Current Structure

```
essays/
├── index.html                                    # Landing page (newest first)
├── README.md                                     # This file
├── what-do-mountains-represent-in-the-bible/     # Theme essay
│   ├── index.html
│   └── images/
├── mark-5-sent-instead-of-kept/                  # Pericope essay (good HTML template)
│   ├── index.html
│   └── images/
├── philippians-3-4-8-the-audit/
│   ├── index.html
│   └── images/
├── genesis-1-overture-in-sevens/
│   ├── index.html
│   └── images/
└── colossians-2-13-15-three-verbs-cross/
    ├── index.html
    └── images/
```

Live site: [https://4toddt.github.io/tools/essays/](https://4toddt.github.io/tools/essays/)

## Recommended Process for a New Essay

1. **Choose a slug**  
   Use a short, descriptive, URL-friendly name. Pericope essays often use passage-based slugs (e.g., `mark-5-sent-instead-of-kept`). Theme essays may use the article question or title (e.g., `what-do-mountains-represent-in-the-bible`).

2. **Create the folder**  
   In the repo, create: `essays/[your-slug]/`

3. **Create the images folder**  
   Inside the new folder, create `images/`.

4. **Generate the images**  
   Use Grok Imagine to create 5–7 images that illustrate the key movements of the argument.  
   - Images should support the exegesis, not decorate it.  
   - Keep a consistent visual style within one essay (same figure style, palette, lighting).  
   - For narrative pericopes: prefer commission / hinge moments over chaos spectacle.  
   - For theme essays: landscapes and conceptual beats are fine; keep ANE material secondary to the biblical claim (polemic, not museum slideshow).

5. **Upload the images**  
   Upload them into the `images/` folder. You can name them descriptively (`hero.jpg`, `parallel.jpg`, etc.) or sequentially. Update the `index.html` to reference the correct filenames.

6. **Create the article page**  
   - Copy `mark-5-sent-instead-of-kept/index.html` (or a recent theme essay) as a starting template.  
   - Replace the `<title>`, meta description, and main heading.  
   - Paste the **exact original text** of your article (no wording changes).  
   - Place the images at the natural breakpoints in the argument (hero at top, then key moments *after* the prose they illustrate).  
   - Keep image captions short, italic, and load-bearing (essay language or a verse), not mere photo labels.  
   - Do not alter the core styling or Tailwind classes unless you have a clear reason.  
   - **Share metadata (recommended):**  
     - `link rel="canonical"` → absolute Pages URL for the essay  
     - Open Graph + Twitter `summary_large_image`  
     - `og:image` / `twitter:image` → **absolute** URL to the hero image  
     - Visible byline + `<time datetime="YYYY-MM-DD">` under the title  
     - `loading="lazy"` on body images (not the hero)

7. **Update the landing page**  
   Edit `essays/index.html` and add a new card/link for the new essay so it appears first on the published essays home page.

8. **Commit & publish**  
   Commit the changes. GitHub Pages will automatically rebuild and deploy the site (usually within 30–60 seconds).

## Styling & Design Principles (Keep It Simple)

- The design prioritizes long-form readability for dense exgetical writing.  
- Greek/Hebrew text receives subtle visual treatment (light background + bottom border) so it stands out without competing with the argument.  
- Images should support the exegesis, not decorate it. Six to seven images per essay is a good working number.  
- Vertical rhythm and breathing room matter more than visual flair.  
- Only make changes that genuinely improve readability or clarity. Avoid changes for their own sake.

## Image Generation Prompts (Template Starting Point)

When generating images, use prompts that are:
- Theologically precise to the specific point being illustrated  
- Cinematic biblical realism with warm, natural lighting  
- Consistent in figure style and palette within one essay  
- For narrative scenes: focused on the healed/sent person and Jesus (or the moment of commission) rather than chaos or demons  

Example structure used for Mark 5:
- Hero image at the boat (the hinge moment of request/refusal)
- Parallel to the calling of the Twelve (Mark 3:14)
- The specific request (“that he might be with him”)
- The commission and sending
- The man heralding in the Decapolis
- Closing image of the man walking the path into Gentile territory

## Future Improvements (When Needed)

- Create a `template/` subfolder with a clean starter `index.html` (including the share-metadata block) so new essays can be duplicated even faster.
- Retrofit OG/canonical/byline onto older essays.
- Add a simple JSON or Markdown index file that the landing page can read dynamically.
- Consider a small script or GitHub Action if the volume of essays grows significantly.

For now, the current manual-but-simple workflow is intentionally lightweight and sufficient for weekly or bi-weekly publishing.

---

Maintained in the `tools` repository. All published essays are served via GitHub Pages from the `/essays` path.
