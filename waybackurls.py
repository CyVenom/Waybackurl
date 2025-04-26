#!/usr/bin/env python3
import requests
import json
from urllib.parse import urlparse
import argparse

def get_host(input_url):
    if not input_url.startswith(('http://', 'https://')):
        input_url = 'http://' + input_url
    return urlparse(input_url).netloc

def waybackurls(host, with_subs):
    target = f"*.{host}" if with_subs else host
    url = f"https://web.archive.org/cdx/search/cdx?url={target}/*&output=json&fl=original&collapse=urlkey"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return [row[0] for row in data[1:]]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('-s', '--subs', action='store_true')
    args = parser.parse_args()
    host = get_host(args.host)
    urls = waybackurls(host, args.subs)
    filename = f"{host}-waybackurls.json"
    with open(filename, 'w') as f:
        json.dump(urls, f, indent=4)
    print(f"[*] Saved results to {filename}" if urls else "[-] Found nothing")
