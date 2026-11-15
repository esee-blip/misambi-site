#!/usr/bin/env python3
"""
Misambi Medical Mission - gallery builder
=========================================

Turns a folder of original photos into a fast, date-organised web gallery.

    python tools/build_gallery.py "C:/path/to/Misambi Files"

What it does, for every photo in the folder (sub-folders included):
  1. Reads the date the photo was taken from EXIF (DateTimeOriginal, then
     DateTimeDigitized, then DateTime). If the photo has no EXIF date it uses the
     file's modified date and marks it as approximate. With --no-file-dates those
     photos go under "Date not available" instead. No date is ever invented.
  2. Writes two web copies, without camera metadata (no GPS or serial numbers):
       images/gallery/thumb/<id>.jpg  - small, for the grid  (max 640 px)
       images/gallery/full/<id>.jpg   - large, for the viewer (max 1800 px)
     Photos that were already processed are skipped, so re-runs are quick.
  3. Skips exact duplicate files (same bytes, different name).
  4. Writes js/gallery-data.js (the list the gallery page reads), refreshes the
     four featured photos in gallery.html, and bumps the cache-busting version.

Captions, featured photos and collection titles live in tools/gallery-config.json.
Needs Python 3.8+ and Pillow:  pip install Pillow
"""
import argparse, hashlib, json, os, re, sys, time
from datetime import datetime
from html import escape

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is not installed. Run:  pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "tools", "gallery-config.json")
OUT_THUMB = os.path.join(ROOT, "images", "gallery", "thumb")
OUT_FULL = os.path.join(ROOT, "images", "gallery", "full")
DATA_JS = os.path.join(ROOT, "js", "gallery-data.js")
GALLERY_HTML = os.path.join(ROOT, "gallery.html")
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
THUMB_MAX, FULL_MAX = 640, 1800
THUMB_Q, FULL_Q = 72, 80
EXIF_IFD = 0x8769
TAGS = [(36867, "DateTimeOriginal"), (36868, "DateTimeDigitized"), (306, "DateTime")]


def load_config():
    if not os.path.exists(CONFIG):
        return {"featured": [], "captions": {}, "collections": {}}
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["captions"] = {k.lower(): v for k, v in cfg.get("captions", {}).items()}
    return cfg


def exif_date(im):
    try:
        ex = im.getexif()
        sub = ex.get_ifd(EXIF_IFD)
    except Exception:
        return None
    for tag, _ in TAGS:
        raw = sub.get(tag) or ex.get(tag)
        if not raw:
            continue
        raw = str(raw).strip().strip("\x00")
        for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y:%m:%d"):
            try:
                d = datetime.strptime(raw[:19] if len(raw) >= 19 else raw, fmt)
                if 1990 <= d.year <= datetime.now().year + 1:
                    return d
            except ValueError:
                pass
    return None


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "photo"


def save(im, path, max_side, quality):
    im = im.copy()
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    return im.size


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="folder with the original photos (sub-folders are included)")
    ap.add_argument("--no-file-dates", action="store_true", help="never fall back to file dates")
    ap.add_argument("--rebuild", action="store_true", help="re-create every thumbnail and full image")
    ap.add_argument("--prune", action="store_true", help="delete web copies whose original is no longer in the folder")
    args = ap.parse_args()

    if not os.path.isdir(args.source):
        sys.exit(f"Folder not found: {args.source}")
    os.makedirs(OUT_THUMB, exist_ok=True)
    os.makedirs(OUT_FULL, exist_ok=True)
    cfg = load_config()

    files = []
    for dirpath, _, names in os.walk(args.source):
        for n in sorted(names):
            if os.path.splitext(n)[1].lower() in EXTS and not n.startswith("."):
                files.append(os.path.join(dirpath, n))
    files.sort()
    print(f"Found {len(files)} photos in {args.source}")

    seen_hash, used_ids, photos = {}, set(), []
    made = skipped = dupes = 0
    t0 = time.time()
    for i, path in enumerate(files, 1):
        with open(path, "rb") as f:
            digest = hashlib.sha1(f.read()).hexdigest()
        if digest in seen_hash:
            dupes += 1
            print(f"  duplicate skipped: {os.path.relpath(path, args.source)} (same as {seen_hash[digest]})")
            continue
        seen_hash[digest] = os.path.relpath(path, args.source)

        try:
            im = Image.open(path)
        except Exception as e:
            print(f"  cannot read {path}: {e}")
            continue
        taken, source = exif_date(im), "exif"
        if not taken and not args.no_file_dates:
            taken, source = datetime.fromtimestamp(os.path.getmtime(path)), "file"
        if not taken:
            source = "none"

        stem = slug(os.path.splitext(os.path.basename(path))[0])
        pid = f"{taken:%Y-%m-%d}-{stem}" if taken else f"undated-{stem}"
        base, n = pid, 2
        while pid in used_ids:
            pid, n = f"{base}-{n}", n + 1
        used_ids.add(pid)

        thumb_p = os.path.join(OUT_THUMB, pid + ".jpg")
        full_p = os.path.join(OUT_FULL, pid + ".jpg")
        src_mtime = os.path.getmtime(path)
        fresh = (not args.rebuild and os.path.exists(thumb_p) and os.path.exists(full_p)
                 and os.path.getmtime(full_p) >= src_mtime)
        if fresh:
            with Image.open(full_p) as f:
                fw, fh = f.size
            with Image.open(thumb_p) as t:
                tw, th = t.size
                bg = t.convert("RGB").resize((1, 1), Image.BOX).getpixel((0, 0))
            skipped += 1
        else:
            im.draft("RGB", (FULL_MAX, FULL_MAX))   # fast JPEG decode at reduced size
            im = ImageOps.exif_transpose(im).convert("RGB")
            fw, fh = save(im, full_p, FULL_MAX, FULL_Q)
            tw, th = save(im, thumb_p, THUMB_MAX, THUMB_Q)
            bg = im.resize((1, 1), Image.BOX).getpixel((0, 0))
            made += 1
        im.close()

        name = os.path.basename(path)
        photos.append({
            "id": pid,
            "src": name,
            "t": f"images/gallery/thumb/{pid}.jpg",
            "f": f"images/gallery/full/{pid}.jpg",
            "w": fw, "h": fh, "tw": tw, "th": th,
            "d": taken.strftime("%Y-%m-%dT%H:%M:%S") if taken else None,
            "ds": source,
            "c": cfg["captions"].get(name.lower(), ""),
            "bg": "#%02x%02x%02x" % tuple(bg[:3]),
        })
        if i % 25 == 0 or i == len(files):
            print(f"  {i}/{len(files)} processed ({time.time() - t0:.0f}s)")

    # newest first; undated last
    photos.sort(key=lambda p: (p["d"] is None, p["d"] or ""), reverse=False)
    dated = sorted([p for p in photos if p["d"]], key=lambda p: p["d"], reverse=True)
    photos = dated + [p for p in photos if not p["d"]]

    if args.prune:
        keep = {p["id"] + ".jpg" for p in photos}
        removed = 0
        for folder in (OUT_THUMB, OUT_FULL):
            for n in os.listdir(folder):
                if n not in keep:
                    os.remove(os.path.join(folder, n)); removed += 1
        print(f"Pruned {removed} old web copies")

    by_src = {p["src"].lower(): p["id"] for p in photos}
    featured = [by_src[s.lower()] for s in cfg.get("featured", []) if s.lower() in by_src][:4]
    for p in photos:                              # top up to four if needed
        if len(featured) >= 4:
            break
        if p["id"] not in featured:
            featured.append(p["id"])

    version = datetime.now().strftime("%Y%m%d%H%M")
    data = {
        "version": version,
        "photos": [{k: v for k, v in p.items() if k != "src"} for p in photos],
        "featured": featured,
        "collections": cfg.get("collections", {}),
    }
    with open(DATA_JS, "w", encoding="utf-8", newline="\n") as f:
        f.write("/* Generated by tools/build_gallery.py - do not edit by hand. */\n")
        f.write("window.MISAMBI_GALLERY = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    update_html(photos, featured, version)
    days = len({p["d"][:10] for p in photos if p["d"]})
    print(f"\nDone: {len(photos)} photos on {days} dates | {made} new web copies, {skipped} unchanged, {dupes} duplicates skipped")
    approx = sum(p["ds"] == "file" for p in photos); none = sum(p["ds"] == "none" for p in photos)
    if approx: print(f"  {approx} photos had no EXIF date; their file date was used")
    if none: print(f"  {none} photos have no date and appear under 'Date not available'")


def nice_date(iso):
    d = datetime.strptime(iso[:10], "%Y-%m-%d")
    return f"{d.day} {d:%B %Y}"


def update_html(photos, featured, version):
    """Write the four featured photos into gallery.html (so they show even before
    JavaScript runs) and bump the ?v= on gallery-data.js / gallery.js."""
    with open(GALLERY_HTML, encoding="utf-8") as f:
        html = f.read()
    by_id = {p["id"]: p for p in photos}
    items = []
    for i, pid in enumerate(featured):
        p = by_id[pid]
        when = nice_date(p["d"]) if p["d"] else "Date not available"
        alt = p["c"] or f"Misambi Medical Mission, {when}"
        cap = escape(p["c"]) if p["c"] else ""
        items.append(
            f'      <a class="mg-feature" href="{p["f"]}" data-id="{pid}" style="--bg:{p["bg"]}">\n'
            f'        <img src="{p["t"] if i else p["f"]}" alt="{escape(alt)}" width="{p["tw"] if i else p["w"]}" height="{p["th"] if i else p["h"]}"{" loading=\"lazy\"" if i else ""} decoding="async">\n'
            f'        <span class="mg-feature-meta"><time datetime="{(p["d"] or "")[:10]}">{when}</time>{"<span>" + cap + "</span>" if cap else ""}</span>\n'
            f'      </a>')
    block = "\n".join(items)
    html, n = re.subn(r"(<!-- gallery:featured:start -->).*?([ \t]*<!-- gallery:featured:end -->)",
                      lambda m: m.group(1) + "\n" + block + "\n" + m.group(2), html, flags=re.S)
    if not n:
        print("  note: featured markers not found in gallery.html; skipped")
    html = re.sub(r'(js/gallery(?:-data)?\.js)\?v=[\w.]+', r'\1?v=' + version, html)
    total = len(photos)
    html = re.sub(r'(data-gallery-total>)\d+(<)', r'\g<1>' + str(total) + r'\2', html)
    with open(GALLERY_HTML, "w", encoding="utf-8", newline="") as f:
        f.write(html)


if __name__ == "__main__":
    main()
