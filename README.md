# design-council

A mixture-of-experts router skill for Claude Code. It sorts a frontend design job, picks one lead expert skill and up to two advisors, writes one shared brief, hands audit, direction, build, specialist and critique work to subagents, and settles conflicts between their rules.

## Install

```bash
git clone https://github.com/shiverin/design-council
cp -R design-council/skills/design-council ~/.claude/skills/
```

The router calls these expert skills, which it expects in `~/.claude/skills/`. Install the ones you want from their own repos:

| Expert | Source | Licence |
|---|---|---|
| impeccable | https://github.com/pbakaus/impeccable | Apache-2.0 |
| unslop | https://github.com/heydamir/unslop (by Damir Sokolovsky) | CC-BY-4.0 |
| hallmark | https://github.com/Nutlope/hallmark | MIT |
| design-taste-frontend | https://github.com/Leonxlnx/taste-skill | MIT |
| frontend-design | https://github.com/anthropics/skills | Apache-2.0 |
| landing-page-design, figma-designer | https://github.com/elayadesign/ai-design-skills | MIT |
| anti-slop-ui | https://github.com/nyrthoughts/anti-slop-design | MIT |

## Contents

```
skills/design-council/SKILL.md            routing table, precedence, 7-step pipeline
skills/design-council/references/         expert roster, shared floor, handoff prompts
skills/design-council/scripts/council_lint.py   portable zero-dependency AI-tell linter
skills/design-council/tests/run.sh        linter tests (bash tests/run.sh)
```

`council_lint.py` replaces anti-slop-design's `lint-tells.sh` on macOS, where BSD grep lacks `-P` and that script's emoji rule silently skips.

## Credits

No expert skill files are copied here. The shared floor and pass order summarise rules from the skills above. The pass-by-pass method and several rules are adapted from Unslop by Damir Sokolovsky (https://github.com/heydamir/unslop), licensed CC-BY-4.0. Test fixtures `bad.tsx` and `clean.tsx` come from anti-slop-design (MIT).

## Licence

MIT.
