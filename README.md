# WaybackURLs

**WaybackURLs** is a simple Python script that queries the Internet Archive’s CDX API to fetch all unique URLs archived under a given domain—and optionally its subdomains—and saves them to a JSON file.

## Features

- Fetch URLs for a single host or for `*.host` (subdomains)
- Outputs a de-duplicated, alphabetical list of URLs
- Easy command-line interface using `argparse`
- Saves results as `<host>-waybackurls.json`

## Requirements

- Python 3.6 or higher
- [`requests`](https://pypi.org/project/requests/) library

## Installation

```bash
# Update package lists and install Python 3 & pip
sudo apt update && sudo apt install python3 python3-pip

# Install the requests library
pip3 install requests
```

## Usage

```bash
# Basic: fetch archived URLs for the exact host
you@machine:~$ python3 waybackurls.py example.com

# Include subdomains (uses -s or --subs flag)
you@machine:~$ python3 waybackurls.py example.com -s
```

### Arguments

- `host` : Domain or URL to query (e.g. `example.com` or `https://example.com/path`)
- `-s`, `--subs` : Include subdomains (queries `*.host/*`)

## Output

On success, generates a file named:

```
<host>-waybackurls.json
```

which contains a pretty-printed JSON array of all archived URLs.

## Examples

```bash
# Exact host only
you@machine:~$ python3 waybackurls.py github.com

# Host + subdomains
you@machine:~$ python3 waybackurls.py github.com --subs
```

## License

This project is licensed under the MIT License. Feel free to reuse and adapt!

