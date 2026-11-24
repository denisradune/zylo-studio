#!/usr/bin/env python3
"""
Viewer ideas from zylo.video, for the daily episode run.

Ideas are sent through the "Suggest a video" form and stored by the site. This script reads them through the
owner-only /api/admin endpoint and records a review status for each one, so no idea is judged twice.
E-mail addresses are never fetched (the request asks the site to redact them); only the idea text, rubric,
optional first name and date come back.

  scripts/ideas.py pending                 # ideas not decided yet (status new or shortlisted), as JSON
  scripts/ideas.py all                     # every idea with its status
  scripts/ideas.py review <id> --status used --video https://youtu.be/... [--note "..."]
  scripts/ideas.py review <id> --status rejected --note "not verifiable"
  scripts/ideas.py review <id> --status shortlisted --note "good, fits rubric 4 day"

Statuses: new | shortlisted | used | rejected. Marking "used" with --video e-mails the viewer (site side,
only if they left an address and Resend is configured).

Credentials: ZYLO_ADMIN_PASSWORD (same value as ADMIN_PASSWORD in Vercel), from the environment or .env.
Site: ZYLO_SITE, default https://zylo.video. If either is missing or storage is off, `pending` prints
{"available": false, ...} and exits 0, so the daily run simply continues without ideas.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env() -> None:
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def call(body: dict) -> dict:
    site = os.environ.get('ZYLO_SITE', 'https://zylo.video').rstrip('/')
    pw = os.environ.get('ZYLO_ADMIN_PASSWORD') or os.environ.get('ADMIN_PASSWORD')
    if not pw:
        raise RuntimeError('ZYLO_ADMIN_PASSWORD is not set')
    req = urllib.request.Request(
        f'{site}/api/admin', data=json.dumps(body).encode(), method='POST',
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {pw}', 'User-Agent': 'zylo-studio/1.0'},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read()).get('error', e.reason)
        except Exception:
            err = e.reason
        raise RuntimeError(f'site answered {e.code}: {err}') from None


def listing(only_pending: bool) -> None:
    try:
        data = call({'action': 'list', 'redact': True})
    except Exception as e:  # noqa: BLE001 - any failure means "no ideas today", never a failed episode
        print(json.dumps({'available': False, 'reason': str(e), 'ideas': []}, indent=1))
        return
    if not data.get('storage') or data.get('storeError'):
        print(json.dumps({'available': False, 'reason': 'site storage is not connected', 'ideas': []}, indent=1))
        return
    rows = []
    for i in data.get('ideas', []):
        st = (i.get('review') or {}).get('status', 'new')
        if only_pending and st not in ('new', 'shortlisted'):
            continue
        rows.append({
            'id': i['id'], 'idea': i.get('idea', ''), 'rubric': i.get('topic', 'other'),
            'name': i.get('name', ''), 'at': i.get('at', ''), 'status': st,
            'note': (i.get('review') or {}).get('note', ''),
        })
    rows.sort(key=lambda r: r['at'])
    print(json.dumps({'available': True, 'count': len(rows), 'ideas': rows}, indent=1, ensure_ascii=False))


def main() -> None:
    load_env()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('pending')
    sub.add_parser('all')
    rv = sub.add_parser('review')
    rv.add_argument('id')
    rv.add_argument('--status', required=True, choices=['new', 'shortlisted', 'used', 'rejected'])
    rv.add_argument('--note', default='')
    rv.add_argument('--video', default='')
    a = ap.parse_args()
    if a.cmd in ('pending', 'all'):
        return listing(a.cmd == 'pending')
    if a.status == 'used' and not a.video:
        sys.exit('--video is required with --status used')
    try:
        print(json.dumps(call({'action': 'review', 'id': a.id, 'status': a.status, 'note': a.note, 'video': a.video}), indent=1))
    except Exception as e:  # noqa: BLE001
        sys.exit(f'review failed: {e}')


if __name__ == '__main__':
    main()
