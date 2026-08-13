# Structure — performance ads agency site

Astro + Tailwind (used only for layout utilities; the visual system itself is
custom CSS in `src/styles/global.css`).

## Structure

```
src/
├── components/       Header, Footer, FooterCTA, FloatingContacts,
│                      LeadForm, WhiteLabelForm, AccountStructureDiagram
├── components/ui/     Breadcrumbs, FAQAccordion
├── config/site.ts     Brand info, nav, form option lists — edit placeholders here
├── layouts/Layout.astro
├── styles/global.css  Design tokens: colors, type scale, buttons, forms
└── pages/             index, services, industries, white-label, how-it-works,
                        about, contact, thank-you, privacy-policy, terms
```

## Before launch

Search the codebase for `[PLACEHOLDER` and fill in:
- Phone, WhatsApp, and email in `src/config/site.ts`
- GTM/GA4/Google Ads IDs in `src/config/site.ts` (`TRACKING`)
- Form backend endpoints in `src/config/site.ts` (`FORM`) — currently forms
  `fetch()` to a placeholder endpoint and expect a 2xx response
- CRM/form-provider name referenced in `privacy-policy.astro`

## Commands

| Command           | Action                          |
| :----------------- | :------------------------------ |
| `npm install`       | Install dependencies            |
| `npm run dev`       | Start dev server at localhost:4321 |
| `npm run build`     | Build to `./dist/`              |
| `npm run preview`   | Preview the production build    |
