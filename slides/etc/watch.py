#!/bin/sh

#############################
# Required modules
# pip install watchdog
# npm install -g mac-chrome
#

#python='echo "Python not found"'
#for p in /usr/local/anaconda3/envs/py37/bin/python /Users/wakita/.pyenv/versions/miniconda-latest/envs/py37/bin/python; do
#    if [ -x "$p" ]; then
#        python=$p; break
#    fi
#done

python << End_of_Python3

import json, os, re, sys, time

from watchdog import events, observers

DEBUG = '--debug' in set(sys.argv)

with open('etc/site.json') as f:
    C = json.load(f)

# Markdown を処理して HTML を生成したのちに、Google Chrome にページのリロードを促す Shell script
PANDOC_CMD = f'''
pandoc \
  --from markdown+smart+footnotes+fenced_code_blocks+fenced_code_attributes \
  --to revealjs --output={C['HTML']} \
  --variable revealjs-url=/y19-vis/lib/reveal.js \
  --css=/y19-vis/lib/reveal.css \
  --slide-level=2 --standalone --mathjax \
  {C['MD']}
chrome-refresh {C['LURL']}'''

def system(cmd):
    if DEBUG: print(cmd)
    os.system(cmd)

os.system(f'open -a "Google Chrome" {C["LURL"]}')
os.system(PANDOC_CMD)

imgfile_re = re.compile('images/.*')

class Handler(events.FileSystemEventHandler):
    def handle(self, ev):
        path = ev.src_path[2:]

        if isinstance(ev, events.FileModifiedEvent):
            # 新しい画像が作成された Docroot に追加
            if imgfile_re.match(path):
                system(f'cp {path} {C["DROOT"]}/{C["PAGE"]}/{path}')

        elif isinstance(ev, events.FileCreatedEvent):
            if path[-3:] == '.md':
                # Markdownファイルが更新されたらPandocを起動してDocrootにHTMLを生成する
                system(PANDOC_CMD)
            elif imgfile_re.match(path):
                # 画像ファイルが追加されたらDocrootに追加
                system(f'cp {path} {C["DROOT"]}/{C["PAGE"]}/{path}')

        elif isinstance(ev, events.FileDeletedEvent):
            if path[-3:] == '.md': pass
            elif imgfile_re.match(path): # 画像ファイルが削除されたら Docroot からも削除
                system(f'rm -f {C["DROOT"]}/{C["PAGE"]}/{path}')

        elif isinstance(ev, events.FileMovedEvent):
            if imgfile_re.match(path): # 画像ファイルが移動されたら Docroot でも移動
                path2 = ev.dest_path[2:]
                system(f'mv {C["DROOT"]}/{path} {C["DROOT"]}/{C["PAGE"]}/{path2}')

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
