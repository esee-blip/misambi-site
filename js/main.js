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

  /* Gallery: category filter */
  var filterBtns = document.querySelectorAll(".filter-btn");
  var items = Array.prototype.slice.call(document.querySelectorAll(".gallery-item"));
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cat = btn.getAttribute("data-filter");
      filterBtns.forEach(function (b) {
        b.classList.toggle("active", b === btn);
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      items.forEach(function (it) {
        var show = cat === "all" || it.getAttribute("data-cat") === cat;
        it.classList.toggle("hidden", !show);
      });
    });
  });

  /* Gallery: lightbox */
  var lb = document.querySelector(".lightbox");
  if (lb && items.length) {
    var lbImg = lb.querySelector("img");
    var lbCap = lb.querySelector("figcaption");
    var current = 0;
    var lastFocus = null;
    var visible = function () { return items.filter(function (it) { return !it.classList.contains("hidden"); }); };
    var show = function (idx) {
      var list = visible();
      if (!list.length) return;
      current = (idx + list.length) % list.length;
      var it = list[current];
      var img = it.querySelector("img");
      lbImg.src = img.getAttribute("src");
      lbImg.alt = img.getAttribute("alt") || "";
      var cap = it.querySelector("figcaption");
      lbCap.textContent = cap ? cap.textContent : "";
    };
    var open = function (it) {
      lastFocus = document.activeElement;
      show(visible().indexOf(it));
      lb.classList.add("open");
      document.body.style.overflow = "hidden";
      lb.querySelector(".lb-close").focus();
    };
    var close = function () {
      lb.classList.remove("open");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    };
    items.forEach(function (it) {
      it.addEventListener("click", function () { open(it); });
      it.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(it); }
      });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(current - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(current + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
  }

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
})();
