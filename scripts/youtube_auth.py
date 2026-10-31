#!/usr/bin/env python3
"""
One-time YouTube OAuth login. Run this YOURSELF on your own computer (it opens a
browser). It prints a refresh token; you paste it into .env as YT_REFRESH_TOKEN.
Claude never sees your password and never runs this step.

  pip install google-auth-oauthlib
  python scripts/youtube_auth.py --client-secrets ~/Downloads/client_secret_XXXX.json
"""
import argparse
import json

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--client-secrets', required=True)
    a = ap.parse_args()
    flow = InstalledAppFlow.from_client_secrets_file(a.client_secrets, SCOPES)
    creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
    client = json.load(open(a.client_secrets))
    client = client.get('installed') or client.get('web')
    print('\nPaste these three lines into .env (and nowhere public):\n')
    print(f"YT_CLIENT_ID={client['client_id']}")
    print(f"YT_CLIENT_SECRET={client['client_secret']}")
    print(f'YT_REFRESH_TOKEN={creds.refresh_token}')


if __name__ == '__main__':
    main()
