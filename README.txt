MISAMBI MEDICAL MISSION - WEBSITE
misambimedicalmission.org
==========================================================================

WHAT'S IN THIS FOLDER
---------------------
  index.html          Home page
  about.html          About: story, mission & vision, values, team, partners
  programs.html       Programs, "a day at a camp", upcoming camps
  get-involved.html   Donate (M-Pesa / bank / card), volunteer, partner, FAQ
  gallery.html        Photo gallery with filters and a pop-up viewer
  contact.html        Contact details, message form, map
  404.html            "Page not found" page
  send.php            Sends the contact form to your email
  .htaccess           Server settings (404 page, HTTPS switch, caching)
  robots.txt, sitemap.xml   Help Google find the site
  css/style.css       All colours, fonts and layout
  js/main.js          Menu, gallery, copy buttons, form messages
  images/             All photos (currently labelled placeholders)

Anything shown with a light yellow highlight and [square brackets] on the
site is a placeholder you still need to replace. The full list is at the
bottom of this file.


1. UPLOAD THE SITE (cPanel hosting)
-----------------------------------
  a) Log in to your hosting control panel (cPanel) and open File Manager.
  b) Open the folder  public_html  (this is your website's root).
     Delete any default "index" or "default" page your host put there.
  c) Click Upload and upload  misambi-website.zip.
  d) Back in File Manager, right-click the zip > Extract, into public_html.
  e) Make sure index.html sits DIRECTLY inside public_html
     (not inside public_html/misambi-website/). If it landed in a
     subfolder, open it, Select All, and Move everything up to public_html.
  f) Settings (top right) > tick "Show Hidden Files" to confirm .htaccess
     was extracted too.
  g) Delete the zip file from public_html.

  Visit  http://misambimedicalmission.org  - the site should appear.

  If the domain is registered with one company and hosted with another,
  set the domain's nameservers (at the registrar) to the ones your hosting
  company gives you. Changes can take a few hours to show everywhere.


2. TURN ON HTTPS (the padlock)
------------------------------
  a) cPanel > SSL/TLS Status > Run AutoSSL (most hosts do this for free).
  b) Once  https://misambimedicalmission.org  opens without a warning,
     open .htaccess and remove the # in front of the three "Rewrite"
     lines under "Force HTTPS". Save. Every visitor now gets the secure
     version.


3. SET UP EMAIL AND THE CONTACT FORM
------------------------------------
  a) cPanel > Email Accounts > create  info@misambimedicalmission.org
     (the site already shows this address).
  b) The form sends to that address. To use a different inbox, open
     send.php and change the line   $to = "info@misambimedicalmission.org";
  c) Test it: fill the form on contact.html. You should see a green
     "Thank you" message and receive the email (check Spam the first time).
     A red message means your host's mail function is off - ask your
     host to enable PHP mail(), or tell me and I'll switch the form to
     a service like Formspree.


4. REPLACE THE TEXT
-------------------
  Open each .html file in a text editor (Notepad++, VS Code, or cPanel's
  File Manager > Edit). Search for  [  to jump to each placeholder.

  Placeholders look like this in the code:
      <span class="ph">[Year]</span>
  Replace the WHOLE thing with your text, e.g.   2019

  The header and footer repeat on every page. Use "Find in Files" /
  "Replace in Files" (Notepad++ or VS Code) to update all pages at once.

  These links also hold placeholder numbers - update them too:
    tel:+254700000000            your phone number (in footer + contact)
    https://wa.me/254700000000   your WhatsApp number, no + or spaces
    href="#" next to Facebook / Instagram   your page links (footer)
    href="#" on "Add your PayPal / giving link"   (get-involved.html)

  When everything is filled in, open css/style.css and delete the
  ".ph { ... }" rule near the top to remove the yellow highlight.


5. THE PHOTOS
-------------
  The site now uses your own photos (placed 29 September 2026). To swap
  one, upload a new photo into the images folder with EXACTLY the same
  name (overwrite it).
  Use .jpg, landscape (except team portraits, which are square).
  Keep each photo under ~300 KB so the site loads fast on mobile data -
  shrink them free at  https://squoosh.app  or  https://tinypng.com.

    hero.jpg            Home page top (text sits on the left side)
    about-story.jpg     Home "Who we are" + About page banner
    volunteer.jpg       About story, Get Involved banner + volunteer section
    cta-bg.jpg          Behind the "Help us reach the next village" band
    program-*.jpg       One per program (camps, mobile, maternal,
                        screening, education, referrals)
    team-1..4.jpg       Square portraits, About page
    gallery-01..12.jpg  Gallery page (01-04 also appear on Home)
    og-image.jpg        Preview picture when the site is shared on
                        WhatsApp/Facebook (already designed, keep it)

  To add more gallery photos: in gallery.html copy one <figure ...> line,
  change the image name, the caption and data-cat (outreach, clinic,
  community or education).

  To show partner logos: in about.html replace each
  <div class="partner">...</div> with
  <div class="partner"><img src="images/partner-name.png" alt="Partner name"></div>


6. ADD YOUR MAP
---------------
  Google Maps > find your office > Share > Embed a map > Copy HTML.
  In contact.html, replace the whole <div class="map-box"> ... </div>
  block with:   <div class="map-box" style="padding:0;border:0">PASTE HERE</div>


7. CHANGING COLOURS OR FONTS
----------------------------
  All colours are at the top of css/style.css (:root). Change a value
  there and it updates everywhere. Main colours:
    --terracotta #B4532A (buttons, accents)   --forest #2F5D50 (green bands)
    --ochre #D99A2B (highlights)              --cream #FBF6EE (background)


PLACEHOLDER CHECKLIST
==========================================================================
On EVERY page (footer):
  [ ] your community / region
  [ ] +254 7XX XXX XXX
  [ ] Physical address, town, county
  [ ] Registration: e.g. NGO / CBO reg. no.

index.html:
  [ ] your community / region
  [ ] Year
  [ ] One or two sentences on how the mission started: who founded it, when, and why.
  [ ] 0,000
  [ ] 00   (x2)
  [ ] 000
  [ ] A short quote from a patient, community leader or volunteer about what the mission has meant to them.
  [ ] Name
  [ ] Village / role

about.html:
  [ ] Tell the founding story here. Who started Misambi Medical Mission, in what year, and what moment or need inspired it?
  [ ] Describe how the work grew: the first camp, the first volunteers, the communities you now serve, and any milestones you are proud of.
  [ ] Explain the meaning of the name "Misambi" if it has one.
  [ ] 0,000+
  [ ] To provide accessible, compassionate and quality healthcare to underserved communities in your region, and to equip families with the knowledge to live healthier lives.
  [ ] Healthy, thriving communities where no one is left without care because of distance or cost.
  [ ] Full name   (x4)
  [ ] Partner logo   (x5)

programs.html:
  [ ] Add a sentence about where you currently work, e.g. which villages, sub-counties or institutions.
  [ ] How often, e.g. every quarter, and roughly how many people each camp serves.
  [ ] if offered
  [ ] name them
  [ ] DD   (x3)
  [ ] Mon   (x3)
  [ ] Camp name or location   (x3)
  [ ] Venue, village   (x3)
  [ ] 8:00am to 4:00pm   (x3)

get-involved.html:
  [ ] Add a line on how donations are managed and reported, e.g. updates after every camp.
  [ ] 000000
  [ ] DONATION
  [ ] Bank name
  [ ] 0000000000
  [ ] Branch
  [ ] SWIFTCODE
  [ ] Add your PayPal / giving link
  [ ] 500
  [ ] 1,000
  [ ] 5,000
  [ ] 50,000

gallery.html:
  [ ] Caption: what, where, when   (x12)

contact.html:
  [ ] two working days
  [ ] +254 7XX XXX XXX
  [ ] Physical address, town, county
  [ ] Mon to Fri, 8:00am to 5:00pm
  [ ] Google Map of your location goes here

Also: gallery captions (edit them in gallery.html), tel: and wa.me links,
social links,
PayPal link, and the map (see sections 4-6).
