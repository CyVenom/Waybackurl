#!/usr/bin/env python3
import requests
import json
import time
import sys
from urllib.parse import urlparse
import argparse
from rich.console import Console
from rich.progress import SpinnerColumn, Progress, TextColumn

console = Console()

def get_host(input_url):
    if not input_url.startswith(('http://', 'https://')):
        input_url = 'http://' + input_url
    return urlparse(input_url).netloc

def waybackurls(host, with_subs):
    target = f"*.{host}" if with_subs else host
    url = f"https://web.archive.org/cdx/search/cdx?url={target}/*&output=json&fl=original&collapse=urlkey"

    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Fetching URLs from Wayback Machine...", start=False)
        progress.start_task(task)

        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            console.print("[bold red][-] Request timed out. Try again later.")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red][-] Request failed: {e}")
            sys.exit(1)

    try:
        data = r.json()
    except json.JSONDecodeError:
        console.print("[bold red][-] Failed to parse JSON from response.")
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
        console.print(f"[bold green][+] {len(urls)} URLs saved to [bold yellow]{filename}[/] in [bold cyan]{elapsed:.2f} seconds.[/]")
    else:
        console.print("[bold red][-] No URLs found for the given host.")
