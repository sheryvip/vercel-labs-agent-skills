(function () {
  "use strict";

  /* ===== Edit these once you have them ===== */
  var CONFIG = {
    whatsapp: "201503331435", // digits only, with country code
    email: ""                 // optional fallback, e.g. "info@sanatechgroup.online"
  };

  var STORAGE_KEY = "sana-lang";
  var root = document.documentElement;

  function readLang() { try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; } }
  function saveLang(l) { try { localStorage.setItem(STORAGE_KEY, l); } catch (e) { /* ignore */ } }
  function lang() { return root.getAttribute("lang") === "en" ? "en" : "ar"; }

  function applyLang(l) {
    root.setAttribute("lang", l);
    root.setAttribute("dir", l === "ar" ? "rtl" : "ltr");
    document.querySelectorAll("[data-ar][data-en]").forEach(function (el) {
      el.textContent = el.getAttribute("data-" + l);
    });
  }

  var saved = readLang();
  if (saved === "en" || saved === "ar") applyLang(saved);

  var toggle = document.querySelector(".lang-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var next = lang() === "ar" ? "en" : "ar";
    applyLang(next); saveLang(next);
  });

  // Mobile menu
  var menuBtn = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.focus();
      }
    });
  }

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  // Preselect service from ?service=web on the contact page
  var serviceSelect = document.getElementById("f-service");
  if (serviceSelect) {
    var map = { web: 0, mobile: 1, system: 2, ai: 3, support: 4, consult: 5 };
    var key = new URLSearchParams(window.location.search).get("service");
    if (key && key in map) serviceSelect.selectedIndex = map[key] + 1;
  }

  // Forms: validate, then hand off to WhatsApp / email.
  // Phase 2 replaces this with saving to the dashboard database.
  var MSG = {
    missing: { ar: "من فضلك املأ كل الحقول المطلوبة.", en: "Please fill in all required fields." },
    sent: { ar: "تمام! بنفتحلك واتساب/الإيميل علشان تبعت الطلب.", en: "Great! Opening WhatsApp/email so you can send your request." },
    notReady: { ar: "شكرًا! الإرسال هيتفعّل قريبًا — لحد ما يتفعّل كلّمنا على بيانات التواصل.", en: "Thanks! Sending will be enabled soon — until then, reach us via the contact details." }
  };
  var TITLES = { contact: "طلب خدمة / Service request", careers: "طلب توظيف / Job application", store: "تنبيه المتجر / Store notify" };

  document.querySelectorAll("form.form").forEach(function (form) {
    var msg = form.querySelector(".form-msg");
    function show(kind, isError) {
      msg.textContent = MSG[kind][lang()];
      msg.classList.toggle("error", !!isError);
      msg.hidden = false;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true, lines = [];
      form.querySelectorAll("input, select, textarea").forEach(function (f) {
        var v = (f.value || "").trim();
        var bad = f.required && (!v || (f.type === "url" && !/^https?:\/\/\S+$/i.test(v)));
        f.setAttribute("aria-invalid", bad ? "true" : "false");
        if (bad) ok = false;
        var label = form.querySelector('label[for="' + f.id + '"]');
        var shown = f.tagName === "SELECT" && f.selectedIndex > 0 ? f.options[f.selectedIndex].textContent : v;
        if (v) lines.push((label ? label.textContent : f.name) + ": " + shown);
      });
      if (!ok) { show("missing", true); var first = form.querySelector('[aria-invalid="true"]'); if (first) first.focus(); return; }

      var text = (TITLES[form.dataset.kind] || "Sana") + "\n" + lines.join("\n");
      var wa = CONFIG.whatsapp.replace(/\D/g, "");
      if (wa) {
        show("sent");
        window.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(text), "_blank", "noopener");
      } else if (CONFIG.email.indexOf("@") > 0) {
        show("sent");
        window.location.href = "mailto:" + CONFIG.email + "?subject=" + encodeURIComponent(TITLES[form.dataset.kind] || "Sana") + "&body=" + encodeURIComponent(text);
      } else {
        show("notReady");
      }
      form.reset();
    });
  });
})();
