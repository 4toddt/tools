# Published Essays – Workflow & Guidelines

This folder contains the published, shareable versions of exegetical articles on biblical passages. The goal is to keep the process simple, consistent, and maintainable so new essays can be added quickly without reinventing layout or structure each time.

## Current Structure

```
essays/
├── index.html                 # Landing page listing all published essays
├── README.md                  # This file (instructions for future essays)
└── mark-5-sent-instead-of-kept/   # Example essay folder
    ├── index.html             # The full article page (exact original text + images)
    └── images/                # All illustrations for that essay
        ├── hero.jpg
        ├── parallel.jpg
        ├── request.jpg
        ├── commission.jpg
        ├── herald.jpg
        └── closing.jpg
```

## Recommended Process for a New Essay

1. **Choose a slug**  
   Use a short, descriptive, URL-friendly name based on the passage (e.g., `mark-5-sent-instead-of-kept`, `matthew-23-hypocrisy`, `john-1-word-made-flesh`).

2. **Create the folder**  
   In the repo, create: `essays/[your-slug]/`

3. **Create the images folder**  
   Inside the new folder, create `images/`.

4. **Generate the images**  
   Use Grok Imagine (in this chat) to create 5–7 images that illustrate the key movements of the exegesis.  
   - Focus on post-healing / commission / proclamation moments rather than dramatic action scenes.  
   - Keep a consistent visual style within one essay (same figure style, palette, lighting).  
   - Good moments to illustrate: the hinge request/refusal, the parallel to another text (e.g., Mark 3:14), the sending, the widening scope of the mission, the closing theological point.

5. **Upload the images**  
   Upload them into the `images/` folder. You can name them descriptively (`hero.jpg`, `parallel.jpg`, etc.) or sequentially. Update the `index.html` to reference the correct filenames.

6. **Create the article page**  
   - Copy `mark-5-sent-instead-of-kept/index.html` as a starting template.  
   - Replace the `<title>`, meta description, and main heading with the new passage/title.  
   - Paste the **exact original text** of your article (no wording changes).  
   - Place the images at the natural breakpoints in the argument (hero at top, then key moments).  
   - Keep image captions short, italic, and lightly descriptive with verse references where helpful.  
   - Do not alter the core styling or Tailwind classes unless you have a clear reason.

7. **Update the landing page**  
   Edit `essays/index.html` and add a new card/link for the new essay so it appears on the published essays home page.

8. **Commit & publish**  
   Commit the changes. GitHub Pages will automatically rebuild and deploy the site (usually within 30–60 seconds).

## Styling & Design Principles (Keep It Simple)

- The design prioritizes long-form readability for dense exegetical writing.  
- Greek text receives subtle visual treatment (light background + bottom border) so it stands out without competing with the argument.  
- Images should support the exegesis, not decorate it. Six images per essay is a good working number.  
- Vertical rhythm and breathing room matter more than visual flair.  
- Only make changes that genuinely improve readability or clarity. Avoid changes for their own sake.

## Image Generation Prompts (Template Starting Point)

When generating images, use prompts that are:
- Theologically precise to the specific point being illustrated  
- Cinematic biblical realism with warm, natural lighting  
- Focused on the healed/sent person and Jesus (or the moment of commission) rather than chaos or demons  
- Consistent in figure style and palette within one essay

Example structure used for Mark 5:
- Hero image at the boat (the hinge moment of request/refusal)
- Parallel to the calling of the Twelve (Mark 3:14)
- The specific request (“that he might be with him”)
- The commission and sending
- The man heralding in the Decapolis
- Closing image of the man walking the path into Gentile territory

## Future Improvements (When Needed)

- Create a `template/` subfolder with a clean starter `index.html` so new essays can be duplicated even faster.
- Add a simple JSON or Markdown index file that the landing page can read dynamically (reduces manual editing when adding many essays).
- Consider a small script or GitHub Action if the volume of essays grows significantly.

For now, the current manual-but-simple workflow is intentionally lightweight and sufficient for weekly or bi-weekly publishing.

---

Maintained in the `tools` repository. All published essays are served via GitHub Pages from the `/essays` path.