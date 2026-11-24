#!/usr/bin/env python3
"""Fetch a paper's page photos + source PDF from R2 and decrypt them.
Usage:
  python3 scripts/fetch-images.py <PAPER> [<PAPER> ...]
PAPER is a paper code like HISDSC303T-2025 or a path like
papers/HISDSC303T-2025. Files land in papers/<CODE>/pages/ and
papers/<CODE>/source.pdf (both gitignored - never committed).
Needs:
  - age on PATH (macOS: brew install age; Ubuntu: sudo apt install age;
    Windows: download age from github.com/FiloSottile/age/releases)
  - the age secret key file, via --key PATH, AGE_KEY_FILE, or the default
    ~/examarchive-age-key (get it from Om on WhatsApp).
Already-downloaded files are skipped, so re-running is safe.
"""
import json, os, subprocess, sys, urllib.request, urllib.error

def fail(msg):
    print("ERROR:", msg); sys.exit(1)

def find_age():
    import shutil
    p = os.environ.get("AGE_BIN") or shutil.which("age")
    if not p:
        fail("age is not installed. macOS: brew install age | Ubuntu: sudo apt install age | "
             "Windows: download it from github.com/FiloSottile/age/releases")
    return p

def find_key(argv_key):
    k = argv_key or os.environ.get("AGE_KEY_FILE") or os.path.expanduser("~/examarchive-age-key")
    if not os.path.isfile(k):
        fail(f"age key file not found: {k}\nGet it from Om on WhatsApp and save it there, "
             "or pass --key <path-to-key-file>.")
    return k

def download(url, dest):
    # r2.dev blocks Python urllib's default User-Agent (403); send a browser one.
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        fail(f"download failed HTTP {e.code}: {url}")
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)

def decrypt(age, key, enc, out, magic, label):
    r = subprocess.run([age, "-d", "-i", key, "-o", out, enc],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        fail(f"decrypt failed for {label}: {r.stderr.decode(errors='replace').strip()}")
    with open(out, "rb") as f:
        head = f.read(len(magic))
    if head != magic:
        fail(f"{label} decrypted but is not a {label.split('.')[-1].upper()} file - wrong key?")
    os.remove(enc)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--key")]
    key_arg = None
    for i, a in enumerate(sys.argv[1:]):
        if a == "--key" and i + 1 < len(sys.argv) - 1:
            key_arg = sys.argv[i + 2]
    if not args:
        fail("usage: python3 scripts/fetch-images.py <PAPER> [<PAPER> ...]")
    age = find_age()
    key = find_key(key_arg)
    for paper in args:
        code = os.path.basename(os.path.normpath(paper))
        pdir = os.path.join("papers", code)
        assets = os.path.join(pdir, "assets.json")
        if not os.path.isfile(assets):
            fail(f"no assets.json for {code} (is the paper in papers/? did you run git-crypt unlock?)")
        data = json.load(open(assets))
        pages_dir = os.path.join(pdir, "pages")
        os.makedirs(pages_dir, exist_ok=True)
        got = skipped = 0
        for url in data["pages"]:
            name = os.path.basename(url)[:-4]  # strip .age
            out = os.path.join(pages_dir, name)
            if os.path.isfile(out):
                skipped += 1; continue
            enc = out + ".age"
            download(url, enc)
            decrypt(age, key, enc, out, b"\x89PNG\r\n\x1a\n", name)
            got += 1
        pdf_done = False
        if data.get("source_pdf"):
            out = os.path.join(pdir, "source.pdf")
            if os.path.isfile(out):
                skipped += 1
            else:
                enc = out + ".age"
                download(data["source_pdf"], enc)
                decrypt(age, key, enc, out, b"%PDF", "source.pdf")
                pdf_done = True
        print(f"{code}: fetched {got} pages, skipped {skipped} already present"
              + (", source PDF fetched" if pdf_done else ""))

if __name__ == "__main__":
    main()
