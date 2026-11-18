#!/usr/bin/env python3
"""council_lint.py - portable, zero-dependency linter for common AI-UI tells.

Usage: python3 council_lint.py <file-or-dir> [...] [--json]
Scans .html .htm .css .scss .jsx .tsx .js .ts .vue .svelte .astro .md(x) files.
Exit 0 clean, 1 findings, 2 usage error.
Suppress a line with a trailing comment containing `council-ignore` or `council-ignore:<rule>`.
"""
import json
import os
import re
import sys

EXTS = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro", ".mdx"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", ".design-council", "coverage", "vendor"}

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F\U00002B50\U00002B06\U00002934\U00002935]"
)

# (rule, severity, regex, flags, optional "unless" regex on the same line)
RULES = [
    ("transition-all", "floor", r"\btransition-all\b|transition(-property)?\s*:\s*all\b", 0, None),
    ("animate-layout-prop", "floor", r"transition(-property)?\s*:\s*[^;]*\b(width|height|top|left|margin)\b", re.I, None),
    ("pulse-non-loader", "floor", r"\banimate-(pulse|ping)\b", 0, r"skeleton|loader|loading|live|status"),
    ("hover-scale", "reflex", r"hover:scale-|:hover[^{]*\{[^}]*scale\(", 0, None),
    ("gradient-text", "floor", r"bg-clip-text[^\"'`]*text-transparent|text-transparent[^\"'`]*bg-clip-text|background-clip\s*:\s*text", re.I, None),
    ("purple-blue-gradient", "floor", r"from-(purple|violet|indigo|fuchsia)-\d+[^\"'`]*to-(blue|cyan|pink|sky|indigo|purple|violet)-\d+|linear-gradient\([^)]*(#(7c3aed|8b5cf6|a855f7|6366f1|9333ea)|purple|violet)", re.I, None),
    ("glow-shadow", "reflex", r"shadow-(purple|violet|indigo|fuchsia|pink|blue|cyan)-\d+|box-shadow\s*:[^;]*rgba\(\s*(1[2-6]\d|9\d)\s*,\s*\d+\s*,\s*2[0-5]\d", re.I, None),
    ("blur-blob", "reflex", r"\bblur-(2xl|3xl)\b[^\"'`]*rounded-full|rounded-full[^\"'`]*\bblur-(2xl|3xl)\b", 0, None),
    ("tracked-caps-label", "floor", r"\buppercase\b[^\"'`]*\btracking-(wide|wider|widest)\b|\btracking-(wide|wider|widest)\b[^\"'`]*\buppercase\b|text-transform\s*:\s*uppercase", 0, None),
    ("arbitrary-spacing", "reflex", r"\b-?(m|p)[trblxy]?-\[\d+(\.\d+)?px\]|\b(gap|space-[xy]|inset|top|left|right|bottom)-\[\d+(\.\d+)?px\]", 0, None),
    ("off-grid-px", "finish", r"\b(margin|padding|gap)(-(top|right|bottom|left))?\s*:\s*[^;]*\b(1[13579]|2[13579]|3[13579]|[3579])px", re.I, None),
    ("welcome-back", "floor", r"welcome\s+back", re.I, None),
    ("hype-word", "floor", r"\b(supercharge[sd]?|revolutioni[sz]e[sd]?|game[- ]chang(er|ing)|next[- ]generation|seamless(ly)?|effortless(ly)?|unleash|unlock (the|your|premium|the power))\b", re.I, None),
    ("vague-cta", "reflex", r">\s*(Learn more|Get started|Click here|Submit)\s*<", re.I, None),
    ("ui-exclamation", "reflex", r">[^<>{}]*[A-Za-z]![^<>{}]*<", 0, r"<!|!=|!important"),
    ("new-badge", "reflex", r">\s*(New|NEW|Beta|BETA|PRO)\s*(✨|\U0001F680|\U0001F525)?\s*<", 0, None),
    ("invented-proof", "floor", r"(trusted by|loved by|used by|join)\s+[\d,.]+\+?\s*(k\b|m\b)?\s*(teams|users|companies|developers|customers)|\b\d+x faster\b|\b99\.9+%\s*uptime", re.I, None),
    ("default-font", "reflex", r"font-family\s*:\s*['\"]?(Inter|Roboto|Arial)\b|fontFamily[^}]*['\"](Inter|Roboto)['\"]|family=(Inter|Roboto)\b", re.I, None),
    ("heavy-heading", "finish", r"<h[1-3][^>]*\bfont-(extrabold|black)\b", 0, None),
    ("mid-dot-meta", "reflex", r"\w\s+[·•]\s+\w[^<\n]*\s[·•]\s", 0, None),
    ("numbered-markers", "finish", r">\s*0[1-9]\s*[./—-]?\s*<", 0, None),
    ("outline-none", "floor", r"\boutline-none\b|outline\s*:\s*(none|0)\b", 0, r"focus-visible|ring"),
    ("lorem", "floor", r"lorem ipsum|\[X\]|123,456|John Doe|Jane Doe|Acme( Inc| Corp)?\b", re.I, None),
]
COMPILED = [(n, s, re.compile(p, f), re.compile(u, re.I) if u else None) for n, s, p, f, u in RULES]


def files_under(path):
    if os.path.isfile(path):
        yield path
        return
    for root, dirs, names in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for n in sorted(names):
            if os.path.splitext(n)[1].lower() in EXTS:
                yield os.path.join(root, n)


def scan(path):
    out = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        print(f"warning: cannot read {path}: {e}", file=sys.stderr)
        return out
    is_css = path.endswith((".css", ".scss"))
    has_reduced_motion = any("prefers-reduced-motion" in l or "motion-reduce" in l or "motion-safe" in l for l in lines)
    animates = False
    for i, line in enumerate(lines, 1):
        ign = re.search(r"council-ignore(?::([\w-]+))?", line)
        def ok(rule):
            return not ign or (ign.group(1) and ign.group(1) != rule)
        if re.search(r"@keyframes|\banimation\s*:|\banimate-(?!none)", line) and not re.search(r"skeleton|loader|loading|spin", line, re.I):
            animates = True
        for name, sev, rx, unless in COMPILED:
            if is_css and name in ("ui-exclamation", "vague-cta", "new-badge", "numbered-markers", "mid-dot-meta"):
                continue
            if rx.search(line) and not (unless and unless.search(line)) and ok(name):
                out.append((path, i, name, sev, line.strip()[:160]))
        if not is_css and EMOJI.search(line) and ok("emoji"):
            out.append((path, i, "emoji", "floor", line.strip()[:160]))
    if animates and not has_reduced_motion:
        out.append((path, 0, "no-reduced-motion", "floor", "file animates but has no prefers-reduced-motion / motion-reduce handling"))
    return out


def main(argv):
    as_json = "--json" in argv
    targets = [a for a in argv if a != "--json"]
    if not targets or any(a in ("-h", "--help") for a in targets):
        print(__doc__.strip())
        return 2
    findings, nfiles = [], 0
    for t in targets:
        if not os.path.exists(t):
            print(f"warning: {t} not found, skipping", file=sys.stderr)
            continue
        for f in files_under(t):
            nfiles += 1
            findings.extend(scan(f))
    if as_json:
        print(json.dumps([dict(zip(("file", "line", "rule", "severity", "text"), x)) for x in findings], indent=1))
    else:
        for f, ln, rule, sev, text in findings:
            print(f"{f}:{ln}: [{sev}:{rule}] {text}")
        counts = {}
        for x in findings:
            counts[x[3]] = counts.get(x[3], 0) + 1
        summary = ", ".join(f"{counts.get(k, 0)} {k}" for k in ("floor", "reflex", "finish"))
        print(f"\n{nfiles} file(s) scanned, {len(findings)} finding(s): {summary}." if findings else f"{nfiles} file(s) scanned, no tells found.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
