# Council floor

The intersection every expert agrees on. Binds every output regardless of lead. Only the user's own
words or a locked project design file may waive a style rule (1-12); rules 13-18 are never waived.
Tags show which experts state the rule: I impeccable, U unslop, H hallmark, T taste, F
frontend-design, L landing-page-design, A anti-slop-ui.

## Style

1. No hue-to-hue gradient on surfaces, no gradient text, no colored glow, colored shadow, blob or orb. (U H A F T)
2. No emoji as icons or label decoration; one icon family, one size, one stroke. (U H A)
3. No one-word accent in a heading (italic, bold or colored single word). (H F A)
4. No tracked uppercase eyebrow or label above every heading; labels are sentence case. (H F U A)
5. No middle-dot-joined meta strings or arrows glued to every link. (H F A)
6. No card inside a card; radius by nesting level, inner = outer - padding (min 4px). (H U A F)
7. Spacing on a 4px grid; no arbitrary one-off values (`mt-[13px]`). (U A L)
8. One neutral ramp, three text roles, one accent used rarely in chrome. (U A F)
9. Type chosen on purpose: one family, two at most; never an unchosen default (Inter/Roboto/system) unless it is the brand. (F A U L)
10. No hype copy (supercharge, unlock, seamless, revolutionize, game-changing, next-generation), no exclamation marks in UI, no greeting headline with emoji. (U A F T)
11. CTAs are verb + object and say what happens ("Export report", not "Learn more"). (F U A T L)
12. No replacement cliche: cream + serif + terracotta, near-black + acid green, broadsheet hairlines, SaaS card kit with identical radius and rgba(0,0,0,.1) shadow. (F A)

## Motion

- Never `transition: all` / `transition-all`; name the properties. (H U A)
- Never animate width, height, top, left or margins; transform and opacity only. (H U)
- No looping pulse/ping/shimmer on anything that is not live or a skeleton loader. (U A)
- At most one entrance moment on load. (F U A)

## Never waived

13. No invented metrics, testimonials, logos, customer counts, case studies or quotes. (H U A T I)
14. Visible `:focus-visible` on every interactive element. (H F)
15. `prefers-reduced-motion: reduce` fallback for every animation; content visible without JS. (H F)
16. Text contrast >= 4.5:1 body, >= 3:1 large text, including text on the accent. (U A)
17. Works at 375/390, 768 and 1280+ with no horizontal scroll; tap targets >= 44px on touch. (H T A)
18. Empty, loading and error states for every data-dependent component. (A I)

## Before handing back

- Run `python3 ~/.claude/skills/design-council/scripts/council_lint.py <files>` and the lead's own
  linter if it has one. Fix every finding or record why it is kept.
- Template test: swap the product name for a competitor's. If the screen still fits, push the
  direction harder in copy, visual and signature.
