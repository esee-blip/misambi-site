# Misambi Medical Mission — website

Static website for **misambimedicalmission.org**. Plain HTML, CSS and JavaScript:
no framework. Upload the files to any web host and it runs. The only build step is
optional: `tools/build_gallery.py` prepares gallery photos (see below).

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | Story, mission and vision, values, team, partners |
| `programs.html` | Programs, how an outreach day works, upcoming camps |
| `get-involved.html` | Donate (M-Pesa, bank, card), volunteer, partner, FAQ |
| `gallery.html` | Date-organised photo gallery: 4 featured photos, "Explore all", full-screen viewer |
| `contact.html` | Contact details, message form, map |
| `404.html` | Page not found |

## Other files

- `css/style.css` — all colours, type and layout. Colour tokens sit in `:root` at the top.
- `js/main.js` — mobile menu, reveal animations, copy buttons, form messages, camp countdown.
- `js/gallery.js` — the gallery page: featured grid, date groups, load-more, viewer.
- `js/gallery-data.js` — generated list of gallery photos. Do not edit by hand.
- `images/gallery/thumb/`, `images/gallery/full/` — generated web copies of gallery photos.
- `tools/build_gallery.py`, `tools/gallery-config.json` — gallery builder and its settings.
- `send.php` — contact-form handler. Needs PHP hosting; set `$to` at the top of the file.
- `.htaccess` — 404 page, caching, and an HTTPS redirect (commented out until SSL is live).
- `images/` — all photos. Replace one by uploading a file with the same name.
- `robots.txt`, `sitemap.xml` — for search engines.
- `README.txt` — the client guide: upload steps, what to edit, and the content checklist.

## Still to fill in

Text in square brackets is a placeholder waiting on the client: contact details,
M-Pesa and bank numbers, impact figures, team names, registration number and
gallery captions. `README.txt` lists every one of them by page.

## Adding photos to the gallery

The gallery is built from a folder of original photos (currently
`Desktop/Misambi Files`, one sub-folder per event). The originals never go on the
website; the builder makes small web copies.

1. Put the new photos in the photos folder (any sub-folder name is fine).
2. Run, from the website folder:

   ```
   pip install Pillow            # first time only
   python tools/build_gallery.py "C:/Users/USER/OneDrive/Desktop/Misambi Files"
   ```

3. Upload `gallery.html`, `js/gallery-data.js` and the new files in
   `images/gallery/thumb/` and `images/gallery/full/`.

The builder:

- reads each photo's capture date from EXIF (`DateTimeOriginal`, then
  `DateTimeDigitized`, then `DateTime`). With no EXIF date it uses the file's
  modified date, and the viewer marks it "(approximate)". Add `--no-file-dates`
  to put those photos under "Date not available" instead. Dates are never invented.
- groups photos by month and day, newest first.
- skips photos it has already processed, so re-runs are quick, and skips exact
  duplicate files.
- removes camera metadata (GPS, serial numbers) from the web copies.
- refreshes the 4 featured photos in `gallery.html` and the cache-busting version.

Captions, the 4 featured photos and a title for each date are set in
`tools/gallery-config.json`, using the original file names. `--prune` deletes web
copies whose original has been removed; `--rebuild` re-creates every copy.

A single photo can be linked directly: `gallery.html#photo=<id>` (the id is
shown in the address bar while the viewer is open).

## Deploying

1. Upload the contents of this repository to `public_html` (cPanel) so `index.html`
   sits at the root.
2. Run AutoSSL, then enable the HTTPS redirect in `.htaccess`.
3. Create the `info@misambimedicalmission.org` mailbox and test the contact form.

On a static host such as Cloudflare Pages or GitHub Pages the site works, but
`send.php` does not run — the form needs a form service instead.
