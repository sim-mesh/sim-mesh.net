#!/usr/bin/env python3
"""The firmware contract, from sim-mesh's CONTRACT.md, as this site's
`_includes/contract.md`, which using-firmware/building.md includes.

sim-mesh keeps the contract beside the code that keeps it; the site shows the
same file. Its title is the page's own, so the first `# ` line goes; links into
the sim-mesh repository go to GitHub; a table of contents goes before the first
section; and the whole is kept from Liquid, which would read `{{` in a code
block as its own.

    python3 _tools/contract.py ../sim-mesh/CONTRACT.md
"""

import os
import re
import sys

REPO = "https://github.com/sim-mesh/sim-mesh"
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "_includes", "contract.md")

LINK = re.compile(r"\]\(([^)\s]+)\)")


def to_github(match):
    target = match.group(1)
    if re.match(r"[a-z]+:", target) or target.startswith("#"):
        return match.group(0)
    path, _, anchor = target.partition("#")
    if path == "README.md":
        url = REPO
    else:
        url = "%s/blob/main/%s" % (REPO, path)
    return "](%s%s)" % (url, "#" + anchor if anchor else "")


def page(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    out, toc = [], False
    for line in lines:
        if not toc and line.startswith("## "):
            out += ["* TOC", "{:toc}", ""]
            toc = True
        out.append(LINK.sub(to_github, line))
    return "{% raw %}\n" + "\n".join(out).strip("\n") + "\n{% endraw %}\n"


def main(argv):
    if len(argv) != 2:
        sys.exit("usage: contract.py <sim-mesh's CONTRACT.md>")
    with open(argv[1], encoding="utf-8") as f:
        text = f.read()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page(text))


if __name__ == "__main__":
    main(sys.argv)
