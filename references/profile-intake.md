# Profile-link intake

This workflow requires a host assistant with web or browser tools. The package does not contain a social-platform crawler, credential importer, browser extension, or official platform API integration. The documented link workflow focuses on Xiaohongshu/RedNote.

## Access and fallback

1. Accept a complete profile URL or a shared message containing one. Open short links normally, then verify the final site and profile identity. Keep sources in the private project; do not publish signed URLs or browser state.
2. Prefer an already-connected browser extension operating on the user's permitted, existing signed-in session. Otherwise try ordinary web reading or the host's built-in browser. A built-in browser is not necessarily the user's signed-in Chrome session. If navigation times out, inspect the opened tab once before concluding that no content loaded.
3. Record the visible name, handle, bio, self-described roles, original follower notation, and observation date. Distinguish following, followers, and cumulative likes/saves. An IP-region label is not evidence of residence.
4. Review pinned and currently visible recent posts, usually up to 12 candidates. Choose three to six that represent different content themes rather than ranking only by interaction counts. Open accessible posts to verify authorship, title, date, cover, named metrics, and any collaboration evidence. When a detail page is inaccessible, retain only what the profile actually showed.
5. Stop dependent collection when login, verification, or access restrictions prevent reading. The user may complete login in their own browser, provide a short recording, or send screenshots. Do not request passwords, authentication codes, cookies, or browser storage. If image placeholders remain after one later check, omit them rather than reconstructing a clear image.
6. Missing portraits, email addresses, or a client list do not block a draft. Missing identity does: an unreadable URL is not a reason to insert the demonstration creator's name or data.

## Interpretation

| Material | Use | When uncertain |
| --- | --- | --- |
| Profile name, account, and counts | Directly observed page or user-supplied evidence | Omit unverified precision |
| Content themes and partnership directions | Suggestions grounded in visible work | Keep them as editable copy |
| Qualifications and career history | Explicit self-description or user confirmation | Do not infer from a single post title |
| Brand collaboration | Clear post evidence or user confirmation | Use `kind: unknown` |
| Brand logos | Official assets after relationship confirmation | Omit the client strip or use confirmed names |
| Contact information | Supplied or explicitly public business details | Do not assemble private contacts from other accounts |
| Visual assets | Clear permitted originals or screenshots | Use a photo-free introduction if necessary |

A downloaded cover is not a complete case screenshot. An avatar is not a portrait. Name an interaction metric only when its label or recognizable icon establishes what it counts.

## Private notes and incremental collection

Write `research.md` with identity checks, observation dates, the accessible page scope, raw values, candidate works, selection reasons, collaboration evidence, suggested copy, and missing items. Save only what the media kit requires.

Use `source`, `as_of`, and optional `provenance` in the brief. Mark partial intake explicitly. Save each usable item as it is collected and deduplicate by verified post ID or source URL. Track complete, title-only, missing-asset, and restricted states separately. A saved file alone does not prove a case is complete. Reuse existing assets on revision and refresh dated statistics when needed.

Give the user a short, specific report of what was accessible and what remains missing. Combine necessary follow-up requests instead of asking a long series of questions.

## Browser integration boundary

The skill supplies selection, evidence handling, and layout; an existing host-supported browser connection supplies access. Use that connection when present. Do not claim it is connected when only a built-in browser is available.

A connection can improve access to signed-in pages, but does not guarantee exact counts, private analytics, or knowledge of contracts. Building a dedicated collection extension is a separate development task, not an existing capability of this package.
