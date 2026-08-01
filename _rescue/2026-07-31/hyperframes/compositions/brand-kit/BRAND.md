# Brand Kit — Default Video Compositions

**Applies to:** EdisonEd, Wolf & Eagle, Andrew Cockburn (personal)

## Design Tokens

| Token | Value |
|---|---|
| Heading font | Montserrat (300–900) |
| Body font | Inter (300–700) |
| Primary | #0066FF |
| Primary dark | #0052CC |
| Primary light | rgba(0,102,255,.06) |
| Heading colour | #111111 |
| Body text | #333333 |
| Text muted | #4A4A4A |
| Text light | #777777 |
| Text faint | #999999 |
| Background | #FFFFFF |
| Canvas | #F7F9FA |
| Border | #E2E6EA |
| Radius | 12px |
| Shadow | 0 1px 3px rgba(0,0,0,.06) |
| Status: red | #DC2626 |
| Status: green | #16A34A |
| Status: amber | #D97706 |

## Visual Rules

- White backgrounds only — no dark sections
- Labels: 11px uppercase Montserrat, letter-spacing .08em, primary blue
- Rule accent: 3px solid #0066FF, 48px wide
- Cards: 1px border, 12px radius, subtle shadow
- Headings: tight letter-spacing (-.02em for h1, -.01em for h2)
- Body: 15px, line-height 1.65, antialiased
- No emojis — use inline SVG icons if needed
- Australian/UK English in all text overlays

## Composition Templates

| Template | Use case |
|---|---|
| `intro.html` | 3-second branded opening (logo/title reveal) |
| `lower-third.html` | Name/title overlay (anchored bottom-left) |
| `section-title.html` | Full-screen section break |
| `outro.html` | 3-second close with CTA |
| `base-style.css` | Shared CSS variables for all compositions |

## Font Loading

Google Fonts URL (for compositions):
```
https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap
```

The producer server bundles Montserrat and Inter locally (included in font data) — no external fetch needed during render.
