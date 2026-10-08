# Kings Web (Next.js + shadcn/ui)

A small UI playground for Kings Development Academy, built with:

- **Next.js 15** (App Router) and **TypeScript**
- **Tailwind CSS v4**, configured in `app/globals.css`
  (no `tailwind.config.*` file is needed)
- **shadcn/ui** project structure: `components.json`, `lib/utils.ts`,
  `components/ui/`

## Run it

```bash
cd my-projects/kings-web
npm install
npm run dev      # http://localhost:3000
npm run build    # production build + type check
```

## Project structure

- `components/ui/` holds shadcn-style UI primitives (the shadcn `ui` alias).
- `components/ui/card.tsx` is the shadcn `Card` primitive.
- `components/ui/integration-card.tsx` is the animated integrations card
  (uses `motion`, `@base-ui/react` and `class-variance-authority`).
- `lib/utils.ts` provides the `cn()` helper (`clsx` + `tailwind-merge`).
- `app/globals.css` imports Tailwind and defines the shadcn theme tokens
  for light and dark mode.
- `app/page.tsx` renders `IntegrationCardDemo`.

## Why `components/ui` matters

`components.json` maps the `ui` alias to `@/components/ui`. The shadcn CLI
(`npx shadcn@latest add <component>`) writes generated primitives there, and
components copied from the shadcn ecosystem (like `integration-card.tsx`)
import their siblings from the same path (`@/components/ui/card`). Keeping
primitives in this folder means those imports resolve without edits, and it
keeps low-level building blocks separate from your own page and feature
components in `components/`.

## Starting a fresh project the standard way

This project was set up by hand because the shadcn registry was unreachable
when it was created. On a normal machine, the equivalent is:

```bash
npx create-next-app@latest my-app --ts --tailwind --eslint --app \
  --import-alias "@/*"
cd my-app
npx shadcn@latest init
npx shadcn@latest add card
npm install motion @base-ui/react class-variance-authority
```

## Using the integration card

```tsx
import IntegrationCardDemo from "@/components/ui/integration-card";

export default function Demo() {
  return <IntegrationCardDemo />;
}
```

Notes:

- It is a client component (`"use client"`), so it can be dropped into a
  Server Component page.
- The centre logo is loaded from `cdn.21st.dev`. Swap those two `<img>`
  sources for your own brand logo (for example, files in `public/`).
- Edit the `integrations` array to show different tools. `x`, `y` and `path`
  use a 564 x 410 coordinate space centred on `(282, 205)`.
