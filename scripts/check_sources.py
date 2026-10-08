#!/usr/bin/env python3
"""Daily link checks only: never copy third-party benchmark data."""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
OUTPUT = Path(__file__).resolve().parents[1] / 'data' / 'source-status.json'
SOURCES = (
    ('Artificial Analysis models', 'https://artificialanalysis.ai/models'),
    ('OpenAI model docs', 'https://platform.openai.com/docs/models'),
    ('ChatGPT help', 'https://help.openai.com/'),
)
def check(name, url, opener=urlopen):
    for method in ('HEAD', 'GET'):
        request = Request(url, method=method, headers={'User-Agent': 'MODEL-ATLAS-link-health/1.0'})
        try:
            with opener(request, timeout=15) as response:
                return {'name': name, 'ok': 200 <= response.status < 400}
        except HTTPError as error:
            if error.code in (405, 501) and method == 'HEAD':
                continue
            return {'name': name, 'ok': False}
        except (URLError, TimeoutError, OSError):
            return {'name': name, 'ok': False}
    return {'name': name, 'ok': False}
def main():
    data = {'checked_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'targets': [check(name, url) for name, url in SOURCES]}
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Checked', len(data['targets']), 'source links;',
          sum(item['ok'] for item in data['targets']), 'reachable')
if __name__ == '__main__':
    main()
