(function () {
  "use strict";

  var STORAGE_KEY = "site-lang";
  var root = document.documentElement;
  var defaultLang = root.getAttribute("lang") === "en" ? "en" : "ar";

  function readLang() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function saveLang(lang) {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* ignore */ }
  }

  function applyLang(lang) {
    root.setAttribute("lang", lang);
    root.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
    document.querySelectorAll("[data-ar][data-en]").forEach(function (el) {
      el.textContent = el.getAttribute("data-" + lang);
    });
  }

  applyLang(readLang() || defaultLang);

  // Language toggle
  var toggle = document.querySelector(".lang-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("lang") === "ar" ? "en" : "ar";
      applyLang(next);
      saveLang(next);
    });
  }

  // Mobile menu
  var menuBtn = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Footer year
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  // Contact form → WhatsApp (or email fallback)
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var name = String(data.get("name") || "").trim();
      var phone = String(data.get("phone") || "").trim();
      var message = String(data.get("message") || "").trim();
      var error = form.querySelector(".form-error");

      if (!name || !phone || !message) {
        if (error) error.hidden = false;
        return;
      }
      if (error) error.hidden = true;

      var text = name + " (" + phone + "):\n" + message;
      var wa = (document.body.getAttribute("data-whatsapp") || "").replace(/\D/g, "");
      var email = document.body.getAttribute("data-email") || "";

      if (wa) {
        window.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(text), "_blank", "noopener");
      } else if (email.indexOf("@") > 0) {
        window.location.href = "mailto:" + email + "?subject=" + encodeURIComponent("Website inquiry") + "&body=" + encodeURIComponent(text);
      }
    });
  }
})();
