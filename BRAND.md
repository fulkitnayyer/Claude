# Clearbid Brand Guide

## Logo concept
The Clearbid mark is a stylised **open circle with a dot** — suggesting clarity, a target/aim, and an aperture (transparency). The word "clear" is set in the primary deep-blue, "bid" in the orange accent. This dual-colour wordmark makes the brand name legible as two words while feeling like one brand.

## Files in `/public`
| File | Use |
|---|---|
| `logo.svg` | Primary horizontal lockup — header on white/light backgrounds |
| `logo-dark.svg` | Reversed white version — footer and dark backgrounds |
| `logo-mark.svg` | Icon/monogram only — favicons, app icons, social avatars |
| `favicon.svg` | Browser tab favicon (SVG) |
| `favicon.ico` | Browser tab favicon (legacy ICO) |
| `og-image.svg` | Default social share card — convert to 1200×630 PNG before launch |

> **Note:** `apple-touch-icon.png` (180×180), `icon-192.png`, and `icon-512.png` need to be generated from `logo-mark.svg` before launch. Use a tool like Inkscape, Figma, or the `sharp` CLI.

## Palette
| Role | Hex | Usage |
|---|---|---|
| Primary (deep blue) | `#1a4f7a` | Headlines, nav, header background, body text |
| Primary dark | `#123655` | Hover states, footer |
| Accent (orange) | `#f97316` | CTA buttons, highlights, the "bid" wordmark |
| Accent hover | `#ea580c` | Button hover state |
| Neutral light | `#f8fafc` | Section backgrounds |
| Neutral border | `#e2e8f0` | Card borders |
| Body text | `#1e293b` | Paragraphs |

## Typography
- **Headings:** Inter (800 weight) — self-hosted via Google Fonts
- **Body:** Inter (400/500 weight)
- Fallback stack: `Inter, system-ui, -apple-system, sans-serif`

## Clear space
Maintain a minimum clear space of **½ the height of the logomark** around all sides of the logo.

## Minimum size
- Logo (horizontal): 120px wide minimum
- Logomark: 24px minimum (16px for favicon — tested)

## What NOT to do
- Do not change the orange accent to any other colour
- Do not stretch or distort the logo
- Do not use the logo on a background where it loses contrast — use the dark version on dark backgrounds
- Do not imply Google affiliation — do not use Google's colour palette as the brand's primary identity
- Do not display the Google Partner badge until it is officially earned and the official Google asset is provided

## Evolving the brand
This is a strong starting point. As the agency grows, consider commissioning a professional logomark iteration that goes beyond the SVG wordmark — but keep the name, colour palette, and transparency concept.
