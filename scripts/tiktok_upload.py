#!/usr/bin/env python3
"""
TikTok cross-posting for zylo (TikTok Content Posting API v2).

Every vertical video (each series part, plus the vertical cut of the full story) goes to TikTok the
calendar day (Asia/Jerusalem) AFTER it went public on YouTube. The daily run calls `post-due`.

  python scripts/tiktok_upload.py --check          # token works? which privacy levels are allowed?
  python scripts/tiktok_upload.py post-due         # post everything whose YouTube day is before today
  python scripts/tiktok_upload.py post-due --dry   # list what would be posted
  python scripts/tiktok_upload.py auth             # ONE-TIME login, run by the owner on their own computer

Credentials (env or .env): TT_CLIENT_KEY, TT_CLIENT_SECRET, TT_REFRESH_TOKEN.
TT_MODE: "direct" (default) posts straight to the profile via video.publish;
         "inbox" sends the video to the TikTok app's inbox/drafts (video.upload) where the owner taps Post.
TT_SINCE: YYYY-MM-DD — only videos that went out on YouTube on/after this day (no backlog flood); default:
          everything not yet on TikTok.
TT_PRIVACY: privacy for direct posts, default PUBLIC_TO_EVERYONE. Until TikTok audits the app, only
            SELF_ONLY is allowed — the script detects that from creator_info and falls back (and says so).

State lives in git: episodes/<slug>/tiktok.json {key: {publish_id, status, postedAt, mode, privacy}}.
"""
import argparse
import datetime as dt
import hashlib
import http.server
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.parse
import webbrowser
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent.parent
TZ = ZoneInfo('Asia/Jerusalem')
API = 'https://open.tiktokapis.com/v2'
SCOPES = 'user.info.basic,video.publish,video.upload'
PY = str(ROOT / '.venv/bin/python')
CHUNK = 10 * 1024 * 1024  # TikTok: chunks 5-64 MB, last chunk may be up to 128 MB
DAILY_MAX = 6  # TikTok caps direct posts per creator per day (~15); stay well under it


def load_env() -> None:
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load(p: Path, default):
    return json.loads(p.read_text()) if p.exists() else default


# ---------- auth ----------

def access_token() -> str:
    load_env()
    missing = [k for k in ('TT_CLIENT_KEY', 'TT_CLIENT_SECRET', 'TT_REFRESH_TOKEN') if not os.environ.get(k)]
    if missing:
        raise SystemExit(f'TikTok not connected: missing {", ".join(missing)} (see scripts/tiktok_upload.py auth)')
    r = requests.post(f'{API}/oauth/token/', data={
        'client_key': os.environ['TT_CLIENT_KEY'],
        'client_secret': os.environ['TT_CLIENT_SECRET'],
        'grant_type': 'refresh_token',
        'refresh_token': os.environ['TT_REFRESH_TOKEN'],
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30)
    j = r.json()
    if 'access_token' not in j:
        raise SystemExit(f'TikTok token refresh failed: {j}')
    if j.get('refresh_token') and j['refresh_token'] != os.environ['TT_REFRESH_TOKEN']:
        print('NOTE: TikTok rotated the refresh token — update TT_REFRESH_TOKEN in the environment settings '
              f'(expires in {j.get("refresh_expires_in", "?")} s).', file=sys.stderr)
    return j['access_token']


def auth() -> None:
    """Owner runs this on their own computer: opens TikTok login, prints the three env lines."""
    load_env()
    key = os.environ.get('TT_CLIENT_KEY') or input('TikTok client key: ').strip()
    sec = os.environ.get('TT_CLIENT_SECRET') or input('TikTok client secret: ').strip()
    port = 8765
    redirect = os.environ.get('TT_REDIRECT_URI', f'http://localhost:{port}/callback/')
    verifier = secrets.token_urlsafe(64)
    # TikTok's desktop PKCE uses the HEX sha256 of the verifier; web apps ignore it.
    challenge = hashlib.sha256(verifier.encode()).hexdigest()
    state = secrets.token_urlsafe(16)
    url = 'https://www.tiktok.com/v2/auth/authorize/?' + urllib.parse.urlencode({
        'client_key': key, 'scope': SCOPES, 'response_type': 'code', 'redirect_uri': redirect,
        'state': state, 'code_challenge': challenge, 'code_challenge_method': 'S256'})
    got: dict = {}
    if redirect.startswith('http://localhost'):
        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                got.update(dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query)))
                self.send_response(200)
                self.end_headers()
                self.wfile.write('Done - go back to the terminal.'.encode())

            def log_message(self, *a):
                pass
        srv = http.server.HTTPServer(('localhost', port), H)
        print('Opening TikTok login...\n', url)
        webbrowser.open(url)
        while 'code' not in got and 'error' not in got:
            srv.handle_request()
    else:
        print('Open this link, log in, then paste the FULL address you land on (here, not in any chat):\n', url)
        got.update(dict(urllib.parse.parse_qsl(urllib.parse.urlparse(input('> ').strip()).query)))
    if got.get('state') != state or 'code' not in got:
        raise SystemExit(f'login failed: {got}')
    r = requests.post(f'{API}/oauth/token/', data={
        'client_key': key, 'client_secret': sec, 'code': got['code'], 'grant_type': 'authorization_code',
        'redirect_uri': redirect, 'code_verifier': verifier,
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30).json()
    if 'refresh_token' not in r:
        raise SystemExit(f'token exchange failed: {r}')
    print(f'\nLogged in (scopes: {r.get("scope")}). Add these three as environment variables:\n')
    print(f'TT_CLIENT_KEY={key}\nTT_CLIENT_SECRET={sec}\nTT_REFRESH_TOKEN={r["refresh_token"]}')


# ---------- posting ----------

def api(tok: str, path: str, body: dict) -> dict:
    r = requests.post(f'{API}{path}', json=body, timeout=60,
                      headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json; charset=UTF-8'})
    j = r.json()
    err = j.get('error', {})
    if err.get('code') not in (None, 'ok'):
        raise RuntimeError(f'{path}: {err}')
    return j.get('data', {})


def creator_info(tok: str) -> dict:
    return api(tok, '/post/publish/creator_info/query/', {})


def caption(m: dict) -> str:
    title = m['title'].replace('#shorts', '').strip()
    tags = [w for w in m.get('description', '').split() if w.startswith('#') and w.lower() != '#shorts']
    tags = list(dict.fromkeys(tags + ['#fyp', '#animation']))[:6]
    return f'{title} {" ".join(tags)}'[:2200]


def send(tok: str, video: Path, m: dict, mode: str, privacy: str) -> str:
    size = video.stat().st_size
    n = max(1, size // CHUNK) if size > CHUNK else 1
    chunk = size if n == 1 else CHUNK
    src = {'source': 'FILE_UPLOAD', 'video_size': size, 'chunk_size': chunk, 'total_chunk_count': n}
    if mode == 'inbox':
        data = api(tok, '/post/publish/inbox/video/init/', {'source_info': src})
    else:
        data = api(tok, '/post/publish/video/init/', {'source_info': src, 'post_info': {
            'title': caption(m), 'privacy_level': privacy,
            'disable_duet': False, 'disable_comment': False, 'disable_stitch': False,
            'video_cover_timestamp_ms': 1500, 'is_aigc': bool(m.get('syntheticMedia')),
        }})
    with video.open('rb') as f:
        for i in range(n):
            start = i * chunk
            body = f.read(chunk if i < n - 1 else size - start)
            end = start + len(body) - 1
            r = requests.put(data['upload_url'], data=body, timeout=600, headers={
                'Content-Type': 'video/mp4', 'Content-Length': str(len(body)),
                'Content-Range': f'bytes {start}-{end}/{size}'})
            if r.status_code not in (200, 201, 206):
                raise RuntimeError(f'chunk {i + 1}/{n} failed: {r.status_code} {r.text[:200]}')
    return data['publish_id']


def wait_status(tok: str, publish_id: str, limit: int = 300) -> str:
    t0 = time.time()
    status = 'PROCESSING_UPLOAD'
    while time.time() - t0 < limit:
        d = api(tok, '/post/publish/status/fetch/', {'publish_id': publish_id})
        status = d.get('status', status)
        if status in ('PUBLISH_COMPLETE', 'SEND_TO_USER_INBOX', 'FAILED'):
            if status == 'FAILED':
                status += f" ({d.get('fail_reason')})"
            return status
        time.sleep(5)
    return status


# ---------- what is due ----------

def vertical(d: Path, key: str) -> Path:
    if key == 'full':
        v = d / 'full/out/short.mp4'
        if not v.exists():
            subprocess.run([PY, str(ROOT / 'scripts/make_series.py'), str(d), '--full-only'], check=True)
        return v
    v = d / key / 'out/short.mp4'
    if not v.exists():
        subprocess.run([PY, str(ROOT / 'scripts/make_series.py'), str(d), '--parts', key[4:], '--no-full'], check=True)
    return v


def due(today: dt.date) -> list[tuple[str, Path, str]]:
    since = dt.date.fromisoformat(os.environ['TT_SINCE']) if os.environ.get('TT_SINCE') else dt.date.min
    items = []
    for d in sorted((ROOT / 'episodes').glob('*/uploads.json')):
        d = d.parent
        yt = load(d / 'uploads.json', {})
        tt = load(d / 'tiktok.json', {})
        meta = load(d / 'metadata.json', {})
        for k, v in yt.items():
            if k in tt or k not in meta:
                continue
            at = v.get('publishAt') or meta[k].get('publishAt')
            if not at:
                continue
            yday = dt.datetime.fromisoformat(at.replace('Z', '+00:00')).astimezone(TZ).date()
            if since <= yday < today:
                items.append((at, d, k))
    return sorted(items)


def post_due(dry: bool, max_n: int) -> int:
    load_env()
    today = dt.datetime.now(TZ).date()
    items = due(today)
    if not items:
        print('TikTok: nothing due')
        return 0
    if dry:
        for at, d, k in items:
            print(f'due: {d.name}/{k} (YouTube {at})')
        return 0
    tok = access_token()
    mode = os.environ.get('TT_MODE', 'direct')
    privacy = os.environ.get('TT_PRIVACY', 'PUBLIC_TO_EVERYONE')
    if mode == 'direct':
        info = creator_info(tok)
        opts = info.get('privacy_level_options') or []
        if privacy not in opts:
            print(f'TikTok: {privacy} not allowed for this app yet (options {opts}); '
                  'the app needs TikTok audit for public posts. Not posting.', flush=True)
            return 0
        maxdur = info.get('max_video_post_duration_sec')
    else:
        maxdur = None
    count = 0
    for at, d, k in items[:max_n]:
        meta = json.loads((d / 'metadata.json').read_text())
        video = vertical(d, k)
        if maxdur:
            dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                        str(video)], capture_output=True, text=True).stdout or 0)
            if dur > maxdur:
                print(f'skip {d.name}/{k}: {dur:.0f}s > TikTok max {maxdur}s')
                continue
        print(f'TikTok {mode}: {d.name}/{k}', flush=True)
        try:
            pid = send(tok, video, meta[k], mode, privacy)
            status = wait_status(tok, pid)
        except RuntimeError as e:
            if 'spam' in str(e).lower() or 'rate' in str(e).lower() or 'limit' in str(e).lower():
                print(f'TikTok limit reached: {e}; the rest goes next run')
                break
            raise
        tt = load(d / 'tiktok.json', {})
        tt[k] = {'publish_id': pid, 'status': status, 'mode': mode,
                 'privacy': privacy if mode == 'direct' else None,
                 'postedAt': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
        (d / 'tiktok.json').write_text(json.dumps(tt, indent=1) + '\n')
        print(f'  -> {status}', flush=True)
        count += 1
    print(f'TikTok: {count} posted, {max(0, len(items) - count)} left')
    return count


def check() -> None:
    tok = access_token()
    mode = os.environ.get('TT_MODE', 'direct')
    info = creator_info(tok)
    print(json.dumps({'mode': mode, 'creator': info.get('creator_username'),
                      'privacy_options': info.get('privacy_level_options'),
                      'max_duration_s': info.get('max_video_post_duration_sec')}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true')
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('post-due')
    p.add_argument('--dry', action='store_true')
    p.add_argument('--max', type=int, default=DAILY_MAX)
    sub.add_parser('auth')
    a = ap.parse_args()
    if a.check:
        check()
    elif a.cmd == 'post-due':
        post_due(a.dry, a.max)
    elif a.cmd == 'auth':
        auth()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
