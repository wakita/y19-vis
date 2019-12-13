#!/bin/sh

#############################
# Required modules
# pip install watchdog
# npm install -g mac-chrome
#

export MD=$1
echo $MD

python << End_of_Python3

import os, sys, time

from watchdog import events, observers

MD = os.getenv('MD')

if len(MD) > 1:
    base = MD.replace('.md', '')
    HTML = f'../docs/slides/{base}.html'
    LURL = f'http://localhost:8000/y19-vis/slides/{base}.html'
else: exit(0)

DEBUG = '--debug' in set(sys.argv)

# Markdown を処理して HTML を生成したのちに、Google Chrome にページのリロードを促す Shell script
PANDOC_CMD = f'''
pandoc \
  --from markdown+smart+footnotes+fenced_code_blocks+fenced_code_attributes \
  --to revealjs --output={HTML} \
  --variable revealjs-url=/y19-vis/lib/reveal.js \
  --css=/y19-vis/lib/reveal.css \
  --slide-level=2 --standalone --mathjax \
  --filter pandoc-citeproc \
  {MD}
chrome-refresh {LURL}'''

def system(cmd):
    if DEBUG: print(cmd)
    os.system(cmd)

os.system(PANDOC_CMD)
os.system(f'open -a "Google Chrome" {LURL}')

class Handler(events.FileSystemEventHandler):
    def handle(self, ev):
        path = ev.src_path[2:]

        if isinstance(ev, events.FileCreatedEvent):
            if path[-3:] == '.md':
                # Markdownファイルが更新されたらPandocを起動してDocrootにHTMLを生成する
                system(PANDOC_CMD)

    def on_any_event(self, ev): self.handle(ev)

observer = observers.Observer()
handler = Handler()
observer.schedule(handler, '.', recursive=True)
observer.start()
try:
    while True: time.sleep(1)
except KeyboardInterrupt: observer.stop()
observer.join()

End_of_Python3
