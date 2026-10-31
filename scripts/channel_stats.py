#!/usr/bin/env python3
"""
Daily audience report: what is working on the channel, and which promised seasons are owed.

  scripts/channel_stats.py            # writes stats/<date>.md + stats/latest.md, appends stats/history.jsonl

For every public upload (from episodes/*/uploads.json, plus anything else on the channel):
  views, likes, comments, age, views/day over the first week (age-fair speed), engagement.
Compares like with like (Shorts part 1s vs part 1s, Shorts vs Shorts, full stories vs full stories):
  HIT  = speed >= 2x the median of its group,  FLOP = speed <= 0.4x.
Per series: part-1 speed, how many part-1 viewers come back for later parts (series retention), full-story speed.
Per theme (series.json "rubric"): average part-1 speed -> what the audience wants more of.
Promises: a series whose finale/last line teases a next season ("season 2", "part 4"...) is OWED until a series
with "sequelOf": <slug> exists; listed with the date the promise went out.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import youtube_upload as yu  # noqa: E402

NOW = dt.datetime.now(dt.timezone.utc)


def parse(ts: str) -> dt.datetime:
    return dt.datetime.fromisoformat(ts.replace('Z', '+00:00'))


def series_index() -> tuple[dict, dict]:
    """video id -> (slug, key); slug -> series info."""
    vids, info = {}, {}
    for sj in sorted((ROOT / 'episodes').glob('*/series.json')):
        d = sj.parent
        s = json.loads(sj.read_text())
        ups = json.loads((d / 'uploads.json').read_text()) if (d / 'uploads.json').exists() else {}
        for k, u in ups.items():
            vids[u['id']] = (d.name, k)
        last = s['parts'][-1]['lines'][-1]['say'] if s.get('parts') else ''
        tease = ' '.join([str(s.get('finale', {}).get('text', '')), str(s.get('finale', {}).get('sub', '')), last, str(s.get('promises', ''))])
        promise = re.search(r'season\s*(\d+|two|three|four)|part\s*(\d+|two|three|four|five)\b', tease, re.I)
        info[d.name] = {
            'title': s.get('title', d.name),
            'rubric': s.get('rubric', 'what-if'),
            'parts': len(s.get('parts', [])),
            'sequelOf': s.get('sequelOf'),
            'promise': promise.group(0) if promise else None,
            'uploads': ups,
        }
    return vids, info


def fetch(yt, ids: list[str]) -> list[dict]:
    out = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part='snippet,statistics,status,contentDetails', id=','.join(ids[i:i + 50])).execute()
        out += r.get('items', [])
    return out


def main():
    yu.load_env()
    yt = yu.service()
    ch = yu.my_channel(yt)
    vids, info = series_index()
    ids = set(vids)
    uploads = ch['contentDetails']['relatedPlaylists']['uploads']
    tok = None
    while True:
        r = yt.playlistItems().list(part='contentDetails', playlistId=uploads, maxResults=50, pageToken=tok).execute()
        ids |= {it['contentDetails']['videoId'] for it in r.get('items', [])}
        tok = r.get('nextPageToken')
        if not tok:
            break

    rows = []
    for v in fetch(yt, sorted(ids)):
        st, sn = v['status'], v['snippet']
        pub = parse(st['publishAt']) if st.get('publishAt') and st['privacyStatus'] != 'public' else parse(sn['publishedAt'])
        if st['privacyStatus'] != 'public' or pub > NOW:
            continue
        age = max((NOW - pub).total_seconds() / 86400, 0.05)
        s = v['statistics']
        views = int(s.get('viewCount', 0))
        slug, key = vids.get(v['id'], (None, None))
        is_full = key == 'full' or (key is None and '#shorts' not in sn['title'].lower())
        rows.append({
            'id': v['id'], 'title': sn['title'], 'slug': slug, 'key': key, 'full': is_full,
            'views': views, 'likes': int(s.get('likeCount', 0)), 'comments': int(s.get('commentCount', 0)),
            'age_days': round(age, 2), 'speed': round(views / min(max(age, 1.0), 7.0), 1),
            'eng': round((int(s.get('likeCount', 0)) + int(s.get('commentCount', 0))) / views * 100, 2) if views else 0.0,
        })

    def tag(group: list[dict]) -> None:
        med = statistics.median([r['speed'] for r in group]) if group else 0
        for r in group:
            r['vs_median'] = round(r['speed'] / med, 2) if med else None
            r['flag'] = 'HIT' if med and r['speed'] >= 2 * med and len(group) >= 3 else ('FLOP' if med and r['speed'] <= 0.4 * med and len(group) >= 3 else '')

    shorts = [r for r in rows if not r['full']]
    fulls = [r for r in rows if r['full']]
    tag(shorts)
    tag(fulls)
    p1 = [r for r in shorts if r['key'] == 'part1']
    med1 = statistics.median([r['speed'] for r in p1]) if p1 else 0

    series = []
    for slug, s in info.items():
        mine = {r['key']: r for r in rows if r['slug'] == slug}
        if not mine:
            continue
        first = mine.get('part1')
        later = [mine[k] for k in sorted(mine) if k.startswith('part') and k != 'part1']
        series.append({
            'slug': slug, 'title': s['title'], 'rubric': s['rubric'],
            'part1_speed': first['speed'] if first else None,
            'part1_vs_median': round(first['speed'] / med1, 2) if first and med1 else None,
            'retention': round(later[-1]['views'] / first['views'], 2) if first and later and first['views'] else None,
            'total_views': sum(r['views'] for r in mine.values()),
            'full_speed': mine['full']['speed'] if 'full' in mine else None,
        })
    series.sort(key=lambda x: -(x['part1_speed'] or 0))

    themes: dict[str, list[float]] = {}
    for x in series:
        if x['part1_speed'] is not None:
            themes.setdefault(x['rubric'], []).append(x['part1_speed'])
    theme_rank = sorted(((k, round(statistics.mean(v), 1), len(v)) for k, v in themes.items()), key=lambda t: -t[1])

    sequels = {s['sequelOf'] for s in info.values() if s.get('sequelOf')}
    owed = []
    for slug, s in info.items():
        if s['promise'] and slug not in sequels and s['uploads']:
            last_key = f"part{s['parts']}"
            when = s['uploads'].get(last_key, {}).get('publishAt') or (json.loads((ROOT / 'episodes' / slug / 'metadata.json').read_text()).get(last_key, {}).get('publishAt'))
            aired = bool(when) and parse(when) <= NOW
            perf = next((x for x in series if x['slug'] == slug), {})
            owed.append({'slug': slug, 'promise': s['promise'], 'finale_at': when, 'aired': aired,
                         'part1_vs_median': perf.get('part1_vs_median')})
    owed.sort(key=lambda o: (not o['aired'], o['finale_at'] or ''))

    today = dt.datetime.now(yu_tz()).date().isoformat()
    out = ROOT / 'stats'
    out.mkdir(exist_ok=True)
    md = [f'# Channel stats — {today}', '', f'{len(rows)} public videos ({len(shorts)} Shorts, {len(fulls)} full stories). '
          'speed = views/day over the first week; vs = speed ÷ median of its group (Shorts or full).', '']
    md += ['## Hits and flops', '']
    flagged = [r for r in rows if r.get('flag')]
    md += [f"- **{r['flag']}** {r['title']} — {r['views']} views, {r['speed']}/day, {r['vs_median']}× median ({r['slug'] or 'not in a series'})" for r in flagged] or ['- none yet (need ≥ 3 comparable videos)']
    md += ['', '## Series (best part 1 first)', '', '| series | theme | part 1 views/day | vs median | parts→ retention | total views | full views/day |', '|---|---|---|---|---|---|---|']
    md += [f"| {x['slug']} | {x['rubric']} | {x['part1_speed']} | {x['part1_vs_median']} | {x['retention']} | {x['total_views']} | {x['full_speed']} |" for x in series]
    md += ['', '## Themes (avg part-1 views/day)', ''] + [f'- {k}: {v} ({n} series)' for k, v, n in theme_rank]
    md += ['', '## Promised seasons still owed', '']
    md += [f"- {o['slug']}: \"{o['promise']}\" — finale {'aired' if o['aired'] else 'airs'} {o['finale_at']}, part 1 at {o['part1_vs_median']}× median" for o in owed] or ['- none']
    md += ['', '## All videos', '', '| title | views | likes | comments | age d | views/day | vs | eng % |', '|---|---|---|---|---|---|---|---|']
    md += [f"| {r['title']} | {r['views']} | {r['likes']} | {r['comments']} | {r['age_days']} | {r['speed']} | {r.get('vs_median')} | {r['eng']} |"
           for r in sorted(rows, key=lambda r: -r['speed'])]
    text = '\n'.join(md) + '\n'
    (out / f'{today}.md').write_text(text)
    (out / 'latest.md').write_text(text)
    with (out / 'history.jsonl').open('a') as f:
        f.write(json.dumps({'date': today, 'videos': rows, 'series': series, 'owed': owed}) + '\n')
    print(text)


def yu_tz():
    from zoneinfo import ZoneInfo
    return ZoneInfo('Asia/Jerusalem')


if __name__ == '__main__':
    main()
