#!/usr/bin/env node

const format = require('util').format;
const fs = require('fs');

const prefix = 'index'

const C = {
  MD: prefix + '.md',

  DROOT: '/Users/wakita/Dropbox/doc/classes/q4-vis/docs',
  LSITE: 'http://localhost:8000/y19-vis',
  GSITE: 'https://wakita.github.io/y19-vis',

  PAGE: 'slides/' + prefix + '.html',
  HTML: '%s/%s',

  LURL: '%s/%s',
  GURL: '%s/%s'
};

C.HTML = format(C.HTML, C.DROOT, C.PAGE);
C.LURL = format(C.LURL, C.LSITE, C.PAGE);
C.GURL = format(C.GURL, C.GSITE, C.PAGE);

fs.writeFileSync('site.json', JSON.stringify(C, null, 2));
