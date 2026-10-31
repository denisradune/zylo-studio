#!/usr/bin/env python3
"""
Upload a finished zylo video with the YouTube Data API v3 (videos.insert, resumable).

Credentials come from .env (or the environment): YT_CLIENT_ID, YT_CLIENT_SECRET,
YT_REFRESH_TOKEN. Get them once with scripts/youtube_auth.py.

  scripts/youtube_upload.py --video out/short.mp4 --meta metadata.json [--thumbnail thumb.png] [--dry-run]
  scripts/youtube_upload.py --check          # verify credentials, print the channel it would post to
  scripts/youtube_upload.py --stats --days 7 # views of recent uploads (for the Sunday pick)

metadata.json: {"title", "description", "tags": [...], "categoryId": "28", "privacy": "public",
                "madeForKids": false, "syntheticMedia": false, "publishAt": null}
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_CHANNEL = 'UCfoc78YxRz1DXNroyI688mA'


def load_env() -> None:
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    load_env()
    missing = [k for k in ('YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN') if not os.environ.get(k)]
    if missing:
        sys.exit(f'missing {", ".join(missing)} in .env — see docs/YOUTUBE-SETUP.md')
    creds = Credentials(
        None,
        refresh_token=os.environ['YT_REFRESH_TOKEN'],
        client_id=os.environ['YT_CLIENT_ID'],
        client_secret=os.environ['YT_CLIENT_SECRET'],
        token_uri='https://oauth2.googleapis.com/token',
    )
    return build('youtube', 'v3', credentials=creds, cache_discovery=False)


def my_channel(yt) -> dict:
    items = yt.channels().list(part='id,snippet,contentDetails', mine=True).execute().get('items', [])
    if not items:
        sys.exit('this Google account has no YouTube channel')
    return items[0]


def body_from(meta: dict) -> dict:
    title = meta['title']
    if len(title) > 100:
        sys.exit(f'title is {len(title)} chars (YouTube max 100)')
    status = {
        'privacyStatus': meta.get('privacy', 'public'),
        'selfDeclaredMadeForKids': bool(meta.get('madeForKids', False)),
        'containsSyntheticMedia': bool(meta.get('syntheticMedia', False)),
        'embeddable': True,
        'license': 'youtube',
    }
    if meta.get('publishAt'):
        status['privacyStatus'] = 'private'
        status['publishAt'] = meta['publishAt']
    return {
        'snippet': {
            'title': title,
            'description': meta['description'],
            'tags': meta.get('tags', []),
            'categoryId': str(meta.get('categoryId', '28')),
            'defaultLanguage': 'en',
            'defaultAudioLanguage': 'en',
        },
        'status': status,
    }


def upload(video: Path, meta: dict, thumbnail: Path | None) -> dict:
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    yt = service()
    ch = my_channel(yt)
    if ch['id'] != EXPECTED_CHANNEL:
        sys.exit(f"token belongs to channel {ch['id']} ({ch['snippet']['title']}), expected {EXPECTED_CHANNEL}")
    media = MediaFileUpload(str(video), mimetype='video/mp4', chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body_from(meta), media_body=media, notifySubscribers=True)
    resp, tries = None, 0
    while resp is None:
        try:
            status, resp = req.next_chunk()
            if status:
                print(f'uploaded {int(status.progress() * 100)}%', flush=True)
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504) and tries < 5:
                tries += 1
                time.sleep(2 ** tries)
                continue
            raise
    vid = resp['id']
    if thumbnail:
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumbnail))).execute()
        except HttpError as e:  # custom thumbnails need a phone-verified channel
            print(f'thumbnail not set: {e}', file=sys.stderr)
    return {'id': vid, 'url': f'https://youtube.com/shorts/{vid}' if meta.get('short') else f'https://youtu.be/{vid}',
            'privacy': resp['status']['privacyStatus']}


def stats(days: int) -> list[dict]:
    yt = service()
    uploads = my_channel(yt)['contentDetails']['relatedPlaylists']['uploads']
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    ids = []
    for it in yt.playlistItems().list(part='contentDetails', playlistId=uploads, maxResults=50).execute()['items']:
        if dt.datetime.fromisoformat(it['contentDetails']['videoPublishedAt'].replace('Z', '+00:00')) >= since:
            ids.append(it['contentDetails']['videoId'])
    if not ids:
        return []
    vids = yt.videos().list(part='snippet,statistics', id=','.join(ids)).execute()['items']
    rows = [{'id': v['id'], 'title': v['snippet']['title'], 'views': int(v['statistics'].get('viewCount', 0))} for v in vids]
    return sorted(rows, key=lambda r: -r['views'])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--video')
    ap.add_argument('--meta')
    ap.add_argument('--thumbnail')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--stats', action='store_true')
    ap.add_argument('--days', type=int, default=7)
    a = ap.parse_args()
    if a.check:
        ch = my_channel(service())
        print(json.dumps({'channel': ch['id'], 'title': ch['snippet']['title'], 'expected': ch['id'] == EXPECTED_CHANNEL}))
        return
    if a.stats:
        print(json.dumps(stats(a.days), indent=1))
        return
    meta = json.loads(Path(a.meta).read_text())
    if a.dry_run:
        print(json.dumps(body_from(meta), indent=1))
        return
    print(json.dumps(upload(Path(a.video), meta, Path(a.thumbnail) if a.thumbnail else None)))


if __name__ == '__main__':
    main()
