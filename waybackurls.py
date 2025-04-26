#!/usr/bin/env python3
import requests
import json
import threading
import itertools
import time
import sys
from urllib.parse import urlparse
import argparse

def get_host(input_url):
    if not input_url.startswith(('http://', 'https://')):
        input_url = 'http://' + input_url
    return urlparse(input_url).netloc

def spinner(msg, event):
    for char in itertools.cycle('|/-\\'):
        if event.is_set():
            break
        sys.stdout.write(f'\r{msg} {char}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')

def waybackurls(host, with_subs):
    target = f"*.{host}" if with_subs else host
    url = f"https://web.archive.org/cdx/search/cdx?url={target}/*&output=json&fl=original&collapse=urlkey"
    
    stop_event = threading.Event()
    spin_thread = threading.Thread(target=spinner, args=(f"[*] Fetching from Wayback Machine for {target}", stop_event))
    spin_thread.start()
    
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
    except requests.exceptions.Timeout:
        stop_event.set()
        print("\n[-] Request timed out. Try again later.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        stop_event.set()
        print(f"\n[-] Request failed: {e}")
        sys.exit(1)

    stop_event.set()
    spin_thread.join()

    try:
        data = r.json()
    except json.JSONDecodeError:
        print("[-] Failed to parse JSON from response.")
        sys.exit(1)

    if len(data) <= 1:
        return []

    return [row[0] for row in data[1:]]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetch URLs archived by Wayback Machine for a given domain.")
    parser.add_argument('host', help='Target domain (e.g., example.com)')
    parser.add_argument('-s', '--subs', action='store_true', help='Include subdomains (wildcard search)')
    args = parser.parse_args()

    host = get_host(args.host)
    start_time = time.time()
    urls = waybackurls(host, args.subs)
    elapsed = time.time() - start_time

    if urls:
        filename = f"{host}-waybackurls.json"
        with open(filename, 'w') as f:
            json.dump(urls, f, indent=4)
        print(f"[+] {len(urls)} URLs saved to {filename} in {elapsed:.2f} seconds.")
    else:
        print("[-] No URLs found for the given host.")
