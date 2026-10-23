#!/usr/bin/env python3
"""Search VISION documentation or atomically refresh the same-origin HTML corpus."""
import argparse
from collections import deque
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

BASE = 'https://docs.vision.tamus.edu/'
ROOT = Path(__file__).resolve().parents[1] / 'references'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links = [], []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in ('p', 'div', 'br', 'li', 'tr', 'pre', 'h1', 'h2', 'h3', 'h4'):
            self.parts.append('\n')
        if tag in ('td', 'th'):
            self.parts.append(' | ')
    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.skip:
            self.skip -= 1
        if tag in ('p', 'div', 'li', 'tr', 'pre', 'h1', 'h2', 'h3', 'h4'):
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)
    def text(self):
        return re.sub(r'\n{3,}', '\n\n', ''.join(self.parts)).strip()

def canonical(link, parent=BASE):
    p = urlsplit(urljoin(parent, link))
    if p.scheme != 'https' or p.netloc != urlsplit(BASE).netloc:
        return None
    if p.query or re.search(r'\.[a-zA-Z0-9]+$', p.path):
        return None
    return urlunsplit((p.scheme, p.netloc, p.path.rstrip('/') + '/', '', ''))

def refresh(limit):
    ROOT.mkdir(parents=True, exist_ok=True)
    queue, seen, records = deque([BASE]), set(), []
    with tempfile.TemporaryDirectory(prefix='vision-refresh-', dir=ROOT) as tmp:
        stage = Path(tmp)
        while queue:
            url = queue.popleft()
            if url in seen:
                continue
            if len(seen) >= limit:
                raise RuntimeError('Page limit exceeded; previous cache preserved. Increase --max-pages.')
            seen.add(url)
            req = Request(url, headers={'User-Agent': 'vision-hpc-docs/1.0'})
            with urlopen(req, timeout=30) as response:
                final = canonical(response.url)
                if not final:
                    raise RuntimeError('Unexpected redirect outside documentation: ' + response.url)
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    raise RuntimeError('Expected HTML: ' + url)
                page = Page()
                page.feed(response.read().decode('utf-8'))
            text = page.text()
            if len(text) < 100:
                raise RuntimeError('Empty documentation page: ' + url)
            name = (urlsplit(url).path.strip('/').replace('/', '__') or 'home') + '.txt'
            stamp = datetime.now(timezone.utc).isoformat()
            (stage / name).write_text(f'Source: {url}\nRetrieved: {stamp}\nFormat: HTML-extracted text; images excluded.\n\n{text}\n')
            records.append({'url': url, 'file': name, 'retrieved': stamp})
            for link in page.links:
                target = canonical(link, final)
                if target and target not in seen:
                    queue.append(target)
        # All fetches must succeed before replacing any existing corpus.
        target, backup = ROOT / 'docs', ROOT / 'docs.previous'
        if backup.exists():
            raise RuntimeError('docs.previous exists; inspect it before refreshing again.')
        (stage / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        if target.exists():
            target.rename(backup)
        try:
            stage.rename(target)
        except Exception:
            if backup.exists():
                backup.rename(target)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    print(f'Refreshed {len(records)} pages in {ROOT / "docs"}')

def search(query, limit):
    terms = query.casefold().split()
    hits = []
    for path in sorted((ROOT / 'docs').glob('*.txt')):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            if all(t in line.casefold() for t in terms):
                hits.append((path, i, lines))
    for path, i, lines in hits[:limit]:
        print(f'{path}:{i+1}\n{lines[0]}')
        print('\n'.join(lines[max(0, i-1):i+3]) + '\n')
    print(f'{len(hits)} matching lines; showing {min(limit, len(hits))}.')
    return 0 if hits else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    s = subs.add_parser('search', help='Case-insensitive AND terms on each line')
    s.add_argument('query')
    s.add_argument('--limit', type=int, default=12)
    r = subs.add_parser('refresh', help='Crawl same-origin linked HTML pages; requires network')
    r.add_argument('--max-pages', type=int, default=150)
    args = parser.parse_args()
    try:
        if args.command == 'search':
            return search(args.query, args.limit)
        refresh(args.max_pages)
        return 0
    except Exception as exc:
        print(f'Error: {exc}. Refresh did not complete; use the existing cache or browser.', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
