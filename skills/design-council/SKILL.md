---
name: design-council
description: Mixture-of-experts router for frontend and UI design. Classifies the job, picks one lead expert skill plus up to two advisors from the installed design skills (impeccable, unslop, hallmark, design-taste-frontend, frontend-design, landing-page-design, figma-designer, anti-slop-ui), writes one shared brief, hands off audit, direction, build, specialist and critique work to subagents, and resolves conflicts between their rules. Use when the user wants the best of every design skill at once, says "design council", "mixture of experts", "combine the design skills", or asks to design, redesign, de-slop, audit or polish a site, landing page, dashboard, app screen, component or Figma file and has not named a single skill.
argument-hint: "[build|redesign|unslop|audit|polish|component|figma|copy|motion] <target or prompt>"
---

# Design council

One router, eight experts, one brief, one writer at a time. The council never runs every expert on
every job: a gate picks the lead whose method fits, advisors contribute only their strongest layer,
and a fresh-context critic judges the result. Expert skills live in `~/.claude/skills/<name>/`.

Read [references/experts.md](references/experts.md) once per run (the roster, what each is best at,
its entry point and its dependencies). Read the other references only when a step says so.

## Precedence (when experts disagree)

1. The user's own words in this conversation.
2. A locked `DESIGN.md` / `design.md` / `PRODUCT.md` in the project.
3. The council floor: [references/floor.md](references/floor.md). Binds every expert, every output.
4. The lead expert's method and rules.
5. Advisors, only inside the layer they were hired for.

A rule from an expert that is not the lead or a hired advisor does not apply. Name every conflict you
resolve in the report as `conflict: <rule A> vs <rule B> -> <winner> (<level>)`.

## Step 1: Gate (classify, then route)

Inspect the project before asking anything: framework, `package.json`, Tailwind config, `:root`
tokens, existing `DESIGN.md`/`PRODUCT.md`, the files that render the target, whether it runs.
Then classify on two axes and take the row from the table.

- **State:** `new` (no UI yet, or user wants a new look) or `existing` (keep the product, fix it).
- **Surface:** `marketing` (landing, company, shop, place), `app` (dashboard, admin, tool, settings),
  `component` (one element), `figma` (work through the Figma MCP), `native` (iOS/Android).

| Job | Lead | Advisors (layer) | Never pair with |
|---|---|---|---|
| new + marketing, software/tech/gaming kind | hallmark | frontend-design (plan review), landing-page-design (conversion structure, copy) | unslop, design-taste-frontend |
| new + marketing, place/product/service, photo-led | design-taste-frontend | frontend-design (plan review), landing-page-design (conversion) | hallmark, unslop |
| new + app screen | impeccable (new-work) | frontend-design (plan review), unslop (dashboard tokens, chart rules) | hallmark |
| existing, heavy slop (many tells across color, type, icons, copy) | unslop | impeccable (detector audit, `harden`), anti-slop-ui (states pass) | hallmark, design-taste-frontend |
| existing, light slop / pre-ship polish | impeccable (`polish`) | unslop (signs list only) | hallmark |
| audit or critique only, no edits | impeccable (`audit`/`critique`) | unslop (signs), anti-slop-ui (checklist), council_lint | — |
| one component | impeccable (relevant command) | unslop (spacing/details tokens) | hallmark full flow |
| figma | figma-designer | frontend-design (direction), landing-page-design (if a landing page) | browser-render experts |
| native iOS/Android | impeccable (native refs) | — | web-only experts |
| no Node / no browser / offline | anti-slop-ui | frontend-design (plan), unslop (rules only, no scripts) | experts whose gates need Chrome |
| single layer ask: type, color, motion, layout, copy, states, perf | impeccable (`typeset`/`colorize`/`animate`/`layout`/`clarify`/`harden`/`optimize`) | unslop (that pass's tokens) | — |

Rules for the gate:

- The user names a skill: it becomes lead, and the table still supplies advisors that do not appear
  in its "never pair" column.
- Hallmark is lead on an existing design only when the user names it (`/hallmark redesign`).
- Two rows fit: pick the row whose lead preserves more of what the user asked to keep, and say why.
- Max 3 experts per run (lead + 2). More is slower and their rules collide.

Announce the routing in three lines before any work:

```
Council · lead: <expert> (<why, one clause>) · advisors: <expert> (<layer>), <expert> (<layer>)
Job: <state> + <surface> · target: <files or route> · tools: node <ver>, browser <yes/no>
Floor: references/floor.md · writer: <who edits which files>
```

## Step 2: Brief (shared context, written once)

Write `.design-council/brief.md` in the project (schema in
[references/handoff.md](references/handoff.md#brief)). Every expert and subagent reads this file
instead of re-deriving context. It holds: product, audience, main job, the real material (and what
is absent: never invent metrics, logos, quotes), constraints, the routing, and the direction once
approved.

## Step 3: Audit (parallel, read-only)

Skip on `new` with no incumbent UI. Otherwise run in parallel:

- `python3 ~/.claude/skills/design-council/scripts/council_lint.py <target>` (portable, no deps).
- The lead's own detector when available: Impeccable `scripts/impeccable` detect/audit, Unslop
  `references/signs.md`, Hallmark `sloplint.mjs --render`.
- When the Agent tool exists, spawn the **Auditor** subagent (handoff.md) for a rendered-screen
  review; it never edits.

Merge into one deduplicated findings list in the brief, each with `file:line`, rule, source expert.
Classify slop as heavy / light / none (Unslop's scale). `none` -> report two or three refinements
with exact values and stop unless the user wants more.

## Step 4: Direction (one voice, then stop)

The lead's direction method produces it, the **Director** subagent drafts it when available, and
frontend-design's plan review is the default advisor check ("would I arrive here for any similar
prompt?" -> revise that part). The direction always contains:

- Product (one sentence) · Character (2-3 words, never clean/modern/sleek/minimal/premium)
- World (place or material that tints neutrals and accent) · Accent (one hex, from product or brand)
- Type (one family, two at most, never an unchosen default) · Moment (1-2 places richness lives)
- Signature (one detail only this product has) · Layout concept (prose + ASCII wireframe)
- Replacement-cliche check: not cream+serif+terracotta, not near-black+acid green, not SaaS card kit

Hallmark leads deal a theme instead (its Steps 3 and 5, the Picks block); Taste leads deal with its
scripts. The dealt result is still written into the brief's direction block.

**Stop and wait for the user's approval** before editing code, unless the user said not to ask or
the run is headless. Use AskUserQuestion when available.

## Step 5: Build (single writer)

The lead runs its own build or pass sequence from its SKILL.md, reading the brief. Exactly one
writer per file at any time:

- Default: the main agent is the writer and applies the lead's method directly.
- Large jobs with independent files: spawn **Builder** subagents, each owning a disjoint file set
  (named in the brief), all on the same brief and direction. Never two builders on one file.
- Advisors contribute through **Specialist** subagents that return a patch plan (exact values,
  `file:line`), not edits; the writer applies it inside the lead's pass order.

Pass order when the lead has none of its own (Unslop's, extended): spacing -> color -> icons -> copy
-> type -> layout -> details -> states and mobile -> visuals -> motion. Finish each pass across the
whole target before the next. Read [references/floor.md](references/floor.md) immediately before
the first edit.

## Step 6: Critique (fresh context)

Spawn the **Critic** subagent (handoff.md) with only the brief, the floor, and the rendered output
or files; it has not seen the build. It returns `ship`, `fix <list>` or `rebuild <reason>`. Apply
one fix batch, re-run `council_lint.py` and the lead's own linter once, and stop. A fabricated pass
is itself slop: report real counts.

No Agent tool: do the critique yourself after re-reading only the brief and floor, and say so.

## Step 7: Report

```
Council · lead <x> · advisors <y>, <z>
Direction: <one line>
Findings: <n> found · <n> fixed · <n> kept (reason each)
Conflicts: <list or none>
Verified: <what was rendered/linted and at which widths> · Not verified: <what was not>
Material ask: <the one real asset that would most improve it>
```

## Handoff mechanics

Subagent roles, prompt templates and the return format are in
[references/handoff.md](references/handoff.md). Every subagent prompt includes: the absolute path
of the brief, the expert SKILL.md path(s) it must read, its role boundary (read-only or the exact
files it may write), and the return format. Subagents start cold: never assume they saw this chat.

## Never

- Run Hallmark and Unslop (or Hallmark and Taste) on the same target in one run.
- Let an advisor's taste override the lead outside its layer.
- Install hooks (Impeccable `hooks on`, Hallmark `install-hook.mjs`) or change settings unasked.
- Invent content: metrics, logos, testimonials, customer counts, quotes.
- Swap one cliche for another; remove decoration only to add new decoration.
- Claim a check ran when it did not.
