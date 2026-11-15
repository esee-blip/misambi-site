/* Misambi Medical Mission — site scripts (no libraries needed) */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");

  /* Mobile navigation */
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* Header shadow once the page scrolls */
  function onScroll() {
    if (header) header.classList.toggle("scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Fade sections in as they scroll into view */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* Copy buttons (Paybill, account numbers) */
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      /* Copies the number shown just before the button */
      var src = btn.previousElementSibling;
      var text = btn.getAttribute("data-copy") || (src ? src.textContent.replace(/[\[\]]/g, "").trim() : "");
      var done = function () {
        var old = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = old; }, 1600);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () {});
      } else {
        var ta = document.createElement("textarea");
        ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  /* Contact form: show result after send.php redirects back */
  var status = document.querySelector(".form-status");
  if (status) {
    var params = new URLSearchParams(window.location.search);
    if (params.get("sent") === "1") {
      status.textContent = "Thank you — your message has been sent. We'll get back to you soon.";
      status.className = "form-status show ok";
    } else if (params.get("error")) {
      status.textContent = "Sorry, your message could not be sent. Please check the form and try again, or email us directly.";
      status.className = "form-status show err";
    }
    /* Preselect the enquiry type from links like contact.html?topic=volunteer */
    var topic = params.get("topic");
    var select = document.getElementById("topic");
    if (topic && select) {
      Array.prototype.forEach.call(select.options, function (o) { if (o.value === topic) select.value = topic; });
    }
  }
  /* ---------- Countdown to the next camp (elements with data-countdown) ---------- */
  var cd = document.querySelector("[data-countdown]");
  if (cd) {
    var start = new Date(cd.getAttribute("data-countdown")).getTime();
    var end = new Date(cd.getAttribute("data-countdown-end") || cd.getAttribute("data-countdown")).getTime();
    var units = ["d", "h", "m", "s"];
    var els = {};
    units.forEach(function (u) { els[u] = cd.querySelector('[data-cd="' + u + '"]'); });
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var set = function (u, val) {
      var el = els[u];
      if (!el || el.textContent === val) return;
      el.textContent = val;
      el.classList.remove("cd-flip");
      void el.offsetWidth; /* restart the animation */
      el.classList.add("cd-flip");
    };
    var timer;
    var tick = function () {
      if (isNaN(start)) return;
      var now = Date.now();
      if (now >= start) {
        clearInterval(timer);
        var live = now < end;
        cd.innerHTML = '<p class="countdown-done">' + (live ? "Happening now &mdash; come along!" : "Thank you to everyone who joined us") + "</p>";
        var tag = document.querySelector(".camp-tag");
        if (tag && !live) tag.lastChild.textContent = "Our first medical camp";
        return;
      }
      var secs = Math.floor((start - now) / 1000);
      set("d", String(Math.floor(secs / 86400)));
      set("h", pad(Math.floor(secs / 3600) % 24));
      set("m", pad(Math.floor(secs / 60) % 60));
      set("s", pad(secs % 60));
    };
    tick();
    timer = setInterval(tick, 1000);
  }
})();
