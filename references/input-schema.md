# Input schema

`brief.json` is UTF-8 JSON. Relative asset paths resolve from the brief's directory. Use local PNG, JPG, WebP, AVIF, or trusted static SVG files. Download permitted remote assets into the private project first and record their origins. Text values are escaped as text, not interpreted as HTML.

The only required profile field is `profile.name`. Do not fill absent information with fictional values. The following is a structural example; replace it with verified material for real work.

```json
{
  "profile": {
    "name": "Creator Name",
    "roles": ["Lifestyle creator"],
    "tags": ["Travel", "Everyday design"],
    "bio": "Suggested positioning based on the supplied work.",
    "description": "A concise, evidence-supported partnership introduction.",
    "accounts": [
      {"platform": "Platform A", "followers": "12.8K", "as_of": "2026-10-11", "source": "evidence/profile.png"}
    ]
  },
  "photos": {"original": "photos/portrait.jpg"},
  "brands": [
    {"id": "brand-a", "name": "Confirmed Client", "confirmed": true, "logo": "logos/client.png", "confirmation_source": "User-confirmed relationship", "source_url": "Official logo source URL"}
  ],
  "cases": [
    {"id": "case-a", "title": "Original post title", "kind": "sponsored", "brand_id": "brand-a", "image": "cases/post.png", "image_type": "screenshot", "source": "User-provided screenshot", "metrics": [{"label": "Likes", "value": "980", "source": "Visible post counter", "show": true}]}
  ],
  "sections": [{"title": "Selected work", "subtitle": "A short explanation of this group.", "case_ids": ["case-a"]}]
}
```

## Profile and optional material

`location`, `roles`, `tags`, `bio`, `description`, `accounts`, and `contact` are optional. A contact entry uses `label` and `value`, with optional `source`; include only supplied or explicitly public business contact details. Omit unknown contact information.

The first three accounts appear in the introduction. Additional accounts follow it in a separate section. Accounts without a platform or a usable follower value are omitted from statistics. Keep counts as strings in their original notation; the builder does not interpret abbreviations or calculate a cross-platform total. Known `as_of` dates appear in the footer.

`photos.original` is the source portrait, `photos.cutout` an optional cutout, and `photos.fit: "contain"` requests full-image fitting. Select an appropriate portrait when multiple images exist; add other real photos in the exported HTML if useful. No photo is a fully supported input.

## Cases, brands, and grouping

| Field | Meaning |
| --- | --- |
| `cases[].kind: sponsored` | A confirmed brand collaboration |
| `cases[].kind: editorial` | Confirmed independent work |
| `cases[].kind: unknown` | An unverified relationship, displayed as Content showcase |
| `cases[].image_type` | `cover`, `screenshot`, or `video_frame`; maintained as provenance |
| `cases[].metrics[].show` | Only literal `true` displays a supplementary metric |
| `brands[].confirmed` | Only literal `true` permits inclusion in the client strip |
| `brands[].confirmation_source` | Evidence of the collaboration, separate from logo provenance |
| `brands[].source_url` | The source of the brand's official logo |

Each brand and each case needs a unique ID within its collection. `brand_id` and `case_ids` must reference existing entries. A sponsored case that references a brand requires that brand to be confirmed. A case's header only uses a brand logo for a confirmed sponsored relationship.

Without `sections`, cases are grouped by their relationship type. Unassigned cases are added under More work in full mode rather than dropped. Customize grouping around the creator's actual content themes when useful.

`settings.brand_limit` defaults to `6`. Order confirmed brands by relevance before building. Set it to `0` for all confirmed brands in compact rows, or another non-negative integer for a different limit. Missing logos are shown as plain brand names; explain this substitution in the delivery notes.

## Provenance and partial intake

Optional top-level `intake` records the input mode, coverage, and meaningful gaps:

```json
{
  "intake": {
    "mode": "screen_recording",
    "status": "partial",
    "missing": ["A clear image for the third selected post"]
  },
  "provenance": {
    "profile.bio": {"status": "suggested", "source": "Themes observed in the supplied posts"}
  },
  "delivery_note": "Profile draft based on the supplied materials."
}
```

Use `observed`, `user_confirmed`, or `suggested` as evidence statuses. These fields support assistant review; the builder does not verify their truth automatically. `delivery_note` is an optional visible footer note. Preview mode also adds its own scope label.

For recordings, store clear frames as ordinary image assets. An account or case may include `source: "recordings/profile.mov"` and `source_time_seconds: 2.4`. The renderer uses the extracted image, not the video. Only use a known recording/data date for `as_of`; record processing time separately when the data date is unknown.

`demo: true` adds a visible fictional-data notice. The default runnable fixtures in `assets/examples/brief.json` and `brief-no-photo.json` use invented data and no portrait. The separate `assets/examples/zoe-cao/` directory is an authorized, redacted real showcase and does not set `demo: true`. New user briefs, original recordings, and extracted frames belong in a separate private project.
