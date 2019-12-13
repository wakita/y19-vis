#!/usr/bin/env python

import sys

from livereload import Server, shell

if len(sys.argv) > 1:
    md = sys.argv[1]
    html = f"../docs/slides/{md.replace('.md', '.html')}"
else: exit(0)

PANDOC_CMD=f'''pandoc
  --from markdown+smart+footnotes+fenced_code_blocks+fenced_code_attributes
  --to revealjs --output={html}
  --variable revealjs-url=/y19-vis/lib/reveal.js
  --css=/y19-vis/lib/reveal.css
  --slide-level=2 --standalone --mathjax
  {md}'''

print(PANDOC_CMD)

server = Server()
server.watch(md, shell(PANDOC_CMD, html))
server.serve()
