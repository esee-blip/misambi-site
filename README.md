# Misambi Medical Mission — website

Static website for **misambimedicalmission.org**. Plain HTML, CSS and JavaScript:
no build step, no framework. Upload the files to any web host and it runs.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | Story, mission and vision, values, team, partners |
| `programs.html` | Programs, how an outreach day works, upcoming camps |
| `get-involved.html` | Donate (M-Pesa, bank, card), volunteer, partner, FAQ |
| `gallery.html` | Photo gallery with category filters and a lightbox |
| `contact.html` | Contact details, message form, map |
| `404.html` | Page not found |

## Other files

- `css/style.css` — all colours, type and layout. Colour tokens sit in `:root` at the top.
- `js/main.js` — mobile menu, gallery filter and lightbox, copy buttons, form messages.
- `send.php` — contact-form handler. Needs PHP hosting; set `$to` at the top of the file.
- `.htaccess` — 404 page, caching, and an HTTPS redirect (commented out until SSL is live).
- `images/` — all photos. Replace one by uploading a file with the same name.
- `robots.txt`, `sitemap.xml` — for search engines.
- `README.txt` — the client guide: upload steps, what to edit, and the content checklist.

## Still to fill in

Text in square brackets is a placeholder waiting on the client: contact details,
M-Pesa and bank numbers, impact figures, team names, registration number and
gallery captions. `README.txt` lists every one of them by page.

## Deploying

1. Upload the contents of this repository to `public_html` (cPanel) so `index.html`
   sits at the root.
2. Run AutoSSL, then enable the HTTPS redirect in `.htaccess`.
3. Create the `info@misambimedicalmission.org` mailbox and test the contact form.

On a static host such as Cloudflare Pages or GitHub Pages the site works, but
`send.php` does not run — the form needs a form service instead.
