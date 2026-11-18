# Expert roster

All paths are under `~/.claude/skills/`. Read an expert's SKILL.md before acting as it or briefing a
subagent as it. Sources and commits: `~/.claude/skills/.design-council-sources.txt`.

| Expert | Best at (hire for this) | Weak at / avoid | Entry | Needs |
|---|---|---|---|---|
| **impeccable** | Broadest command set; deterministic detector; audit, critique, polish, harden, typeset, colorize, animate, layout, adapt, optimize; native iOS/Android; DESIGN.md/PRODUCT.md init | Heavy context loader; overkill for a 2-line fix | `impeccable/SKILL.md` -> Setup -> Commands table (`reference/<cmd>.md`); `reference/craft-floor.md` before any edit | `scripts/impeccable` launcher downloads a pinned engine binary from GitHub releases on first run (checksummed). Telemetry: set `DO_NOT_TRACK=1` |
| **unslop** | Existing screens with heavy slop; 9 ordered passes with exact tokens; dashboards and app chrome; chart rules; direction from product "world"; RTL | Greenfield pages; image-heavy marketing without an image tool | `unslop/SKILL.md` Run it; `references/signs.md` (audit), `references/tokens.md` (values) | Optional Node scripts (`snapshot.mjs`; story video needs Playwright + ffmpeg). CC-BY-4.0: keep the credit |
| **hallmark** | New pages from scratch; non-waivable Floor; dealt themes so builds do not converge; sloplint in a real browser; fresh-context hero/finish reviews | Existing designs (only on explicit `/hallmark redesign`); conflicts with unslop and taste | `hallmark/SKILL.md` Flow 0-7; `references/gates.md` | Node 18+; render tier needs `puppeteer-core` + Chrome/Chromium |
| **design-taste-frontend** | Photo-led company, place, product and service sites; copy layer (`copy-lint.mjs`); dealt palettes/heroes; browser finish gate | Dogmatic; breaks SaaS design systems; mandates hover lift/zoom that unslop bans; conflicts with hallmark | `design-taste-frontend/SKILL.md` section 4 The run | Node 22+, Chrome/Edge/Chromium. Ships a skill-scoped Stop hook that runs `scripts/gate.mjs` while the skill is active |
| **frontend-design** | Plan-first: 4-6 hex palette, type roles, ASCII layout, then review the plan against the brief; cliche calibration list; UI writing rules | No enforcement, no tooling | `frontend-design/SKILL.md` Process | Nothing |
| **landing-page-design** | Landing-page intake, section structure, conversion rules, copywriting, SEO/AEO, strict numeric type/spacing/radius rules | Landing pages only; some arbitrary rules; mandatory tagline-reveal section (B11) is a lead-only rule, ignore it as an advisor | `landing-page-design/SKILL.md` A1-A8 (strategy), B1-B10 (visual) | Nothing |
| **figma-designer** | Work inside Figma via the Figma MCP: variables, text styles, auto layout, components, two-layer color tokens | Code output | `figma-designer/SKILL.md` Workflow + Checklist | Figma MCP connector |
| **anti-slop-ui** | Zero-dependency 8-pass cleanup; DESIGN.md template; 15-tell catalog | Shallow compared to unslop | `anti-slop-ui/SKILL.md`; `templates/DESIGN.md`; `docs/ai-tells.md` | Nothing. Its `scripts/lint-tells.sh` emoji rule needs GNU `grep -P` and silently skips on macOS; use `design-council/scripts/council_lint.py` instead |

## Layers an advisor can be hired for

| Layer | Best source | Second source |
|---|---|---|
| Audit / detection | impeccable detector + `audit` | unslop `signs.md`, council_lint |
| Direction | unslop Direction (existing), frontend-design Process (new) | impeccable `shape`/`init` |
| Spacing, radius, details tokens | unslop `tokens.md` + passes 1, 7 | landing-page-design B2-B3 |
| Color | unslop pass 2 | impeccable `colorize` |
| Typography | impeccable `typeset` | unslop pass 5, landing-page-design B1 |
| Copy | design-taste-frontend copy layer (`copy-voice.md`, `copy-lint.mjs`) for marketing; frontend-design writing rules + impeccable `clarify` for app UI | landing-page-design A5 |
| Conversion structure | landing-page-design A2-A4 | hallmark `anatomy.md` |
| Layout / composition | hallmark `layout.md` + macrostructures (new) | impeccable `layout` (existing) |
| States, edge cases, i18n | impeccable `harden`, `onboard` | anti-slop-ui pass 7 |
| Motion | impeccable `animate` | unslop pass 9 |
| Data viz / charts | unslop pass 7 chart rules | hallmark `data-viz.md` |
| Responsive / devices | impeccable `adapt` | hallmark `responsive.md` |
| Performance | impeccable `optimize` | design-taste-frontend `perf.mjs` |
| Final review | hallmark `review-finish.md` (fresh context) | impeccable `critique` |

## Known rule conflicts and their council resolution

| Conflict | Resolution |
|---|---|
| Taste house rule 5 (cards lift 2px, photos zoom 1.02) vs unslop/anti-slop "no hover:scale on cards" | Taste lead: Taste wins on its own pages. Any other lead: no scale on cards; photo zoom inside a fixed frame is allowed |
| Hallmark "never an eyebrow / tracked caps" vs a brand that uses them | Locked DESIGN.md or the user wins (precedence 1-2) |
| Unslop weights 400/500 (600 rare) vs landing-page-design type styles | Lead decides; floor only bans 700-900 headings when the lead is unslop or anti-slop-ui |
| Hallmark ~80 words/screen vs Taste 60-80 words/screen (tech) vs landing pages with long copy | The lead's number; advisors never impose a word budget |
| landing-page-design B11 mandatory tagline-reveal section | Applies only when it is lead |
| frontend-design "brief wins, even a cliche look" vs bans | Precedence 1: the user's explicit request wins over every ban except floor rules on invented content and accessibility |
