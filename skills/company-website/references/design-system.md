# Design System

All visual decisions live as CSS custom properties at the top of `styles.css`. Change tokens, not individual rules.

## Color

| Token | Purpose | Default |
|---|---|---|
| `--brand` | Buttons, links, accents | `#0f766e` |
| `--brand-ink` | Text on `--brand` | `#ffffff` |
| `--bg` | Page background | `#ffffff` |
| `--surface` | Cards, alternating sections | `#f6f7f9` |
| `--text` | Body text | `#111827` |
| `--muted` | Secondary text | `#4b5563` |
| `--border` | Dividers, card outlines | `#e5e7eb` |

Dark mode overrides are in the `@media (prefers-color-scheme: dark)` block.

### Ready palettes by industry

| Industry | `--brand` | Feel |
|---|---|---|
| Tech / software | `#2563eb` | Trust, clarity |
| Construction / real estate | `#b45309` | Solid, warm |
| Medical / clinics | `#0e7490` | Clean, calm |
| Finance / legal | `#1e3a8a` | Serious, premium |
| Food / restaurants | `#c2410c` | Appetite, energy |
| Beauty / fashion | `#be185d` | Elegant |
| Education | `#7c3aed` | Creative |
| Logistics / industry | `#0f766e` | Reliable |

Check contrast of `--brand-ink` on `--brand` (must be ≥ 4.5:1). Darken the brand color if it fails.

## Typography

- Arabic: `"IBM Plex Sans Arabic"` (default), `Cairo`, or `Tajawal`
- English: `Inter`
- Scale (fluid): `--step-0` body 1rem → `--step-4` hero heading `clamp(2rem, 5vw, 3.5rem)`
- Arabic needs a slightly larger line height (1.8) than English (1.6); the template sets this via `:lang(ar)`.
- Never use letter-spacing on Arabic text, and never use all-caps styling on it.

## Spacing & Layout

- Container: `max-width: 72rem`, side padding `1rem` (phone) → `1.5rem`.
- Section padding: `clamp(3rem, 8vw, 6rem)` vertical.
- Grid: `repeat(auto-fit, minmax(16rem, 1fr))` for services and features. It wraps to one column on phones with no media queries.
- Radius `--radius: 14px`; shadow only on hover/raised cards.

## RTL Rules

- Set `dir="rtl"` on `<html>` for Arabic. Use logical properties only:
  `padding-inline`, `margin-inline-start`, `inset-inline-end`, `text-align: start`.
- Mirror directional icons (arrows) with `[dir="rtl"] .icon-arrow { transform: scaleX(-1); }`.
- Do not mirror logos, phone numbers, or media controls.
- Phone numbers: wrap in `<bdi dir="ltr">` so `+20` stays on the left.

## Imagery

- Prefer real photos of the team, office and work over stock images.
- Export WebP/AVIF at 2x the display size, under ~200 KB each.
- Always set `width`, `height`, `alt`; use `loading="lazy"` except for the hero image.
