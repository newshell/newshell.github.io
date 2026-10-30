#!/usr/bin/env python3
"""Validate public static HTML, internal assets and basic credential leaks."""
from html.parser import HTMLParser
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.scripts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for k in ('href','src'):
            if k in a:self.links.append((tag,a[k]))
        if tag=='script' and a.get('src','').startswith(('https://','http://')):self.scripts.append(a['src'])
bad=[]
html_files=sorted(ROOT.glob('**/*.html'))
for file in html_files:
    raw=file.read_text(encoding='utf-8')
    if '<html lang=' not in raw:bad.append(f'{file}: missing lang')
    p=Links();p.feed(raw)
    if p.scripts:bad.append(f'{file}: remote scripts not allowed')
    for tag,link in p.links:
        if not link.startswith('/') or link.startswith('//'):continue
        path=link.split('?',1)[0].split('#',1)[0]
        target=ROOT/path.lstrip('/')
        if target.is_dir():target=target/'index.html'
        if not target.is_file():bad.append(f'{file}: missing {path}')
    for label,regex in (
        ('private IP',r'(?<![0-9.])(?:192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![0-9.])'),
        ('credential',r'\b(?:ghp|gho|ghs)_[A-Za-z0-9]{20,}|\bsk-[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        ('internal identifier',r'(?i)\b(?:UIH_SH_|nvoglv64|m_uiDataVersion|ivtGlBrickPlugin)\b'),
    ):
        if re.search(regex,raw):bad.append(f'{file}: {label}')
if len(html_files)<8:bad.append(f'Only {len(html_files)} HTML pages')
if bad:
    print('\n'.join(bad));sys.exit(1)
print(f'Validated {len(html_files)} static pages, local assets and basic privacy patterns.')
