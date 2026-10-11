# Build, export, and review

## Dependencies

HTML generation uses Python 3 and its standard library. Image export requires Node.js, Playwright, and compatible Chromium. Use existing host runtimes when available; never copy machine-specific paths from another user's environment. Fonts and their licenses are bundled for local rendering.

`PLAYWRIGHT_MODULE_PATH` can point to an existing Playwright module directory. `CHROME_PATH` can point to an installed Chrome executable; otherwise the renderer uses Playwright's installed Chromium. If dependencies are missing, install them in an independent tools directory as shown in the README, subject to the host's permissions. If no browser can run, deliver HTML and explicitly mark PNG/JPG export as incomplete.

## Commands

Replace `<skill>` with the actual skill folder. Keep the user's project outside it.

```sh
python3 <skill>/scripts/build.py --input /project/brief.json --output /project/output-v1 --styles cream-ugc,red-editorial,long-table --mode preview
node <skill>/scripts/render.cjs --input /project/output-v1/manifest.json
```

For a selected full kit, set one style ID and `--mode full`. For eight complete versions, use `--styles all --mode full`. The CLI defaults to all/full; the assistant explicitly selects its usual three-preview workflow. Use a new output directory for revisions. A directory containing a manifest is rejected to protect an existing delivery.

## Files

| Path | Purpose |
| --- | --- |
| `<style>/poster.html` | Editable layout |
| `<style>/poster.png`, `poster.jpg` | Exported images |
| `overview.jpg`, `index.html` | Comparison view and links to layouts |
| `assets/` | Images, fonts, and license notices used by the output |
| `manifest.json` | Build manifest |
| `checks.json` | Basic rendering checks after successful exports |
| `source-brief.json` | Private copy of the original input |

Share HTML together with its assets folder. PNG and JPG can be sent independently. Rebuilding requires the original project images or updated brief paths; the saved brief is provenance, not a self-contained replacement for the input project.

## Visual verification

The renderer checks image loading, horizontal page overflow, and script errors. It does not determine whether a design looks good or a claim is accurate. Inspect the actual exports:

1. Verify names, roles, account figures, and dates against their sources.
2. Check long English names and labels for awkward wrapping or clipping. Preserve framed photo backgrounds and readable foreground information.
3. Check original screenshots, aspect ratios, and logo identity. Avoid stretching images.
4. Confirm full mode preserves every case, and preview mode displays its limited scope. Confirm the configured brand limit.
5. Check additional platform rows, long titles, and multi-line roles for collisions.
6. Review at a realistic phone viewing size. Reduce columns or provide additional sections when necessary, retaining the complete long image.

Templates use a 1080-pixel canvas. Adapt exported HTML/CSS for unusually long content rather than squeezing important text into an unreadable fixed cover. Single-project adjustments do not require changing the skill's source templates.

Run behavioral tests with `python3 <skill>/scripts/test_build.py`. Use the fictional brief in `assets/examples/brief.json` for public demonstrations.
