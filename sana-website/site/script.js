(function () {
  "use strict";

  /* ===== Settings: edit these ===== */
  var CONFIG = {
    whatsapp: "201503331435", // digits only, with country code
    email: "",                // optional fallback, e.g. "info@sanatechgroup.online"
    chatEndpoint: ""          // Sana Assistant Worker URL, e.g. "https://sana-chat.<your-subdomain>.workers.dev"
                              // Empty = guided assistant without AI (still useful, sends to WhatsApp)
  };

  var root = document.documentElement;
  root.classList.add("js");
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { /* storage unavailable */ }
    return null;
  }
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function waLink(text) { return "https://wa.me/" + CONFIG.whatsapp + "?text=" + encodeURIComponent(text); }

  /* ===== Language ===== */
  var langListeners = [];
  function lang() { return root.getAttribute("lang") === "en" ? "en" : "ar"; }
  function L(ar, en) { return lang() === "en" ? en : ar; }
  function applyLang(l) {
    root.setAttribute("lang", l);
    root.setAttribute("dir", l === "ar" ? "rtl" : "ltr");
    $$("[data-ar][data-en]").forEach(function (el) { el.textContent = el.getAttribute("data-" + l); });
    $$("[data-ph-ar]").forEach(function (el) { el.setAttribute("placeholder", el.getAttribute("data-ph-" + l)); });
    langListeners.forEach(function (fn) { fn(l); });
  }
  var savedLang = store("sana-lang");
  if (savedLang === "en" || savedLang === "ar") applyLang(savedLang);
  var langBtn = $(".lang-toggle");
  if (langBtn) langBtn.addEventListener("click", function () {
    var next = lang() === "ar" ? "en" : "ar";
    applyLang(next); store("sana-lang", next);
  });

  /* ===== Theme (light / dark) ===== */
  var darkQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return !!(darkQuery && darkQuery.matches);
  }
  var themeBtn = $(".theme-toggle");
  function syncTheme() { if (themeBtn) themeBtn.setAttribute("aria-pressed", String(isDark())); }
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var next = isDark() ? "light" : "dark";
    root.setAttribute("data-theme", next); store("sana-theme", next); syncTheme();
  });
  if (darkQuery && darkQuery.addEventListener) darkQuery.addEventListener("change", syncTheme);
  syncTheme();

  /* ===== Mobile menu ===== */
  var menuBtn = $(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); }
    });
  }

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  /* ===== Moving identity: progress bar, rotating S, sparkle on reveal ===== */
  var ticking = false;
  function onScroll() {
    ticking = false;
    var max = root.scrollHeight - root.clientHeight;
    var y = window.scrollY || root.scrollTop;
    root.style.setProperty("--progress", max > 0 ? (y / max).toFixed(4) : "0");
    if (!reduceMotion) root.style.setProperty("--spin", Math.min(y / 4, 180).toFixed(1));
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.25 });
    $$(".section, .page-hero, .hero").forEach(function (s) { io.observe(s); });
  }

  /* ===== Shared service data (assistant + quiz) ===== */
  var SV = {
    web: { ar: "المواقع والمتاجر الإلكترونية", en: "Websites & online stores",
      dar: "بنعمل مواقع سريعة واحترافية ومتاجر جاهزة للبيع أونلاين، بتشتغل كويس على الموبايل.",
      den: "We build fast, professional websites and ready-to-sell online stores that work great on mobile.",
      war: "علشان العملاء يلاقوك على جوجل ويطلبوا منك أونلاين.", wen: "so customers find you on Google and order online.",
      kw: ["موقع", "ويب", "متجر", "صفحه", "دومين", "استضافه", "اونلاين", "website", "site", "web", "store", "domain", "hosting", "ecommerce", "landing"] },
    mobile: { ar: "تطبيقات الموبايل", en: "Mobile apps",
      dar: "بنعمل تطبيقات Android و iOS بتجربة استخدام بسيطة لعملائك وفريقك.",
      den: "We build Android and iOS apps with a simple experience for your customers and team.",
      war: "علشان عملاءك يوصلولك بضغطة من موبايلهم.", wen: "so customers reach you with one tap.",
      kw: ["تطبيق", "ابلكيشن", "ابليكيشن", "موبايل", "اندرويد", "ايفون", "app", "android", "ios", "iphone", "mobile"] },
    system: { ar: "أنظمة إدارة الأعمال", en: "Business systems",
      dar: "أنظمة بتنظّم شغلك: مبيعات، مخازن، حسابات، وعملاء — في مكان واحد وبتقارير واضحة.",
      den: "Systems that organise sales, inventory, accounts and customers in one place, with clear reports.",
      war: "كل البيع والمخزون والفلوس في مكان واحد وبتقارير واضحة.", wen: "all sales, stock and money in one place with clear reports.",
      kw: ["نظام", "سيستم", "مخزن", "مخزون", "حسابات", "فواتير", "فاتوره", "كاشير", "نقاط بيع", "جرد", "erp", "crm", "pos", "inventory", "invoice", "accounting", "system"] },
    ai: { ar: "الذكاء الاصطناعي والبوتات", en: "AI & chatbots",
      dar: "مساعدين أذكياء وبوتات واتساب بترد على عملائك 24 ساعة وتنجز المهام المتكررة بدالك.",
      den: "Smart assistants and WhatsApp bots that answer customers around the clock and handle repetitive tasks.",
      war: "يرد على العملاء 24 ساعة وينظّم الطلبات بدالك.", wen: "it answers customers 24/7 and organises orders for you.",
      kw: ["ذكاء", "بوت", "شات", "رد الي", "رد تلقائي", "اوتوماتيك", "اتمته", "ai", "bot", "chatbot", "agent", "automation", "gpt", "claude"] },
    support: { ar: "الدعم الفني والشبكات", en: "IT support & networks",
      dar: "تركيب وصيانة الأجهزة والشبكات وكاميرات المراقبة، ودعم فني تقدر تعتمد عليه.",
      den: "Installation and maintenance of devices, networks and CCTV, with support you can rely on.",
      war: "شبكة ثابتة وأجهزة شغالة من غير توقف.", wen: "a stable network and devices that keep working.",
      kw: ["شبكه", "نت", "انترنت", "راوتر", "واي فاي", "كاميرا", "كاميرات", "مراقبه", "صيانه", "جهاز", "لابتوب", "كمبيوتر", "طابعه", "network", "wifi", "router", "cctv", "camera", "repair", "laptop", "pc", "printer", "support"] },
    consult: { ar: "الاستشارات والتحول الرقمي", en: "Consulting & digital transformation",
      dar: "بنساعدك تختار التقنية الصح لشغلك ونمشي معاك خطوة بخطوة.",
      den: "We help you choose the right technology for your business and guide you step by step.",
      war: "نحدد أولوياتك ونرتّب الخطوات صح من الأول.", wen: "we set your priorities and order the steps right.",
      kw: ["استشاره", "خطه", "ابدا", "تحول رقمي", "نصيحه", "consult", "advice", "plan", "strategy", "digital"] }
  };
  var SV_ORDER = ["web", "mobile", "system", "ai", "support", "consult"];
  function norm(s) {
    return String(s || "").toLowerCase().replace(/[أإآ]/g, "ا").replace(/ة/g, "ه").replace(/ى/g, "ي").replace(/[ً-ْ]/g, "");
  }
  function matchService(text) {
    var n = norm(text), best = null, score = 0;
    SV_ORDER.forEach(function (k) {
      var s = 0;
      SV[k].kw.forEach(function (w) { if (n.indexOf(norm(w)) !== -1) s += w.length > 3 ? 2 : 1; });
      if (s > score) { score = s; best = k; }
    });
    return best;
  }

  /* ===== Contact preselect + forms (to WhatsApp) ===== */
  var serviceSelect = document.getElementById("f-service");
  if (serviceSelect) {
    var key = new URLSearchParams(window.location.search).get("service");
    var idx = SV_ORDER.indexOf(key);
    if (idx !== -1) serviceSelect.selectedIndex = idx + 1;
  }
  var TITLES = { contact: "طلب خدمة / Service request", careers: "طلب توظيف / Job application", store: "تنبيه المتجر / Store notify" };
  $$("form.form").forEach(function (form) {
    var msg = form.querySelector(".form-msg");
    function show(ar, en, isError) {
      msg.textContent = L(ar, en); msg.classList.toggle("error", !!isError); msg.hidden = false;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true, lines = [];
      $$("input, select, textarea", form).forEach(function (f) {
        var v = (f.value || "").trim();
        var bad = f.required && (!v || (f.type === "url" && !/^https?:\/\/\S+$/i.test(v)));
        f.setAttribute("aria-invalid", bad ? "true" : "false");
        if (bad) ok = false;
        var label = form.querySelector('label[for="' + f.id + '"]');
        var shown = f.tagName === "SELECT" && f.selectedIndex > 0 ? f.options[f.selectedIndex].textContent : v;
        if (v) lines.push((label ? label.textContent : f.name) + ": " + shown);
      });
      if (!ok) {
        show("من فضلك املأ كل الحقول المطلوبة.", "Please fill in all required fields.", true);
        var first = form.querySelector('[aria-invalid="true"]'); if (first) first.focus();
        return;
      }
      var text = (TITLES[form.dataset.kind] || "Sana") + "\n" + lines.join("\n");
      if (CONFIG.whatsapp) {
        show("تمام! بنفتحلك واتساب علشان تبعت الطلب.", "Great! Opening WhatsApp so you can send your request.");
        window.open(waLink(text), "_blank", "noopener");
      } else if (CONFIG.email.indexOf("@") > 0) {
        show("تمام! بنفتحلك الإيميل علشان تبعت الطلب.", "Great! Opening email so you can send your request.");
        window.location.href = "mailto:" + CONFIG.email + "?subject=" + encodeURIComponent(TITLES[form.dataset.kind] || "Sana") + "&body=" + encodeURIComponent(text);
      }
      form.reset();
    });
  });

  /* ===== Before / after slider ===== */
  $$(".ba").forEach(function (ba) {
    var range = $(".ba-range", ba);
    if (!range) return;
    function set() { ba.style.setProperty("--pos", range.value + "%"); }
    range.addEventListener("input", set); set();
  });

  /* ===== Savings calculator ===== */
  var calc = document.getElementById("calc-form");
  if (calc) {
    var DAYS = 26, HOURS_PER_MONTH = 176, SAVED_SHARE = 0.4;
    var emp = document.getElementById("calc-emp"), hrs = document.getElementById("calc-hours"), sal = document.getElementById("calc-salary");
    function fmt(n, digits) {
      return new Intl.NumberFormat(lang() === "en" ? "en-US" : "ar-EG", { maximumFractionDigits: digits || 0 }).format(n);
    }
    function updateCalc() {
      var e = +emp.value, h = +hrs.value, s = +sal.value;
      var hours = e * h * DAYS * SAVED_SHARE;
      var month = hours * (s / HOURS_PER_MONTH);
      [emp, hrs, sal].forEach(function (inp) {
        var out = calc.querySelector('output[for="' + inp.id + '"] bdi');
        if (out) out.textContent = fmt(+inp.value, 1);
      });
      var cur = L(" جنيه", " EGP");
      $("#out-hours").textContent = fmt(hours);
      $("#out-month").textContent = fmt(month) + cur;
      $("#out-year").textContent = fmt(month * 12) + cur;
    }
    calc.addEventListener("input", updateCalc);
    langListeners.push(updateCalc);
    updateCalc();
  }

  /* ===== Quiz: "find your solution in 60 seconds" ===== */
  var quiz = document.getElementById("quiz-form");
  if (quiz) {
    var steps = $$(".quiz-step", quiz), qi = 0;
    var bar = $(".quiz-bar span", quiz.parentNode), result = $(".quiz-result", quiz.parentNode);
    var qErr = $(".form-msg", quiz);
    var back = $('[data-quiz="back"]', quiz), next = $('[data-quiz="next"]', quiz), done = $('[data-quiz="done"]', quiz);
    function showStep(i) {
      qi = i;
      steps.forEach(function (s, k) { s.classList.toggle("active", k === i); });
      bar.style.setProperty("--done", ((i + 1) / steps.length * 100) + "%");
      back.hidden = i === 0; next.hidden = i === steps.length - 1; done.hidden = i !== steps.length - 1;
      qErr.hidden = true;
    }
    function answered(i) { return !!steps[i].querySelector("input:checked"); }
    function needAnswer() { qErr.textContent = L("اختار إجابة علشان نكمّل.", "Pick an answer to continue."); qErr.hidden = false; }
    next.addEventListener("click", function () { if (!answered(qi)) return needAnswer(); showStep(qi + 1); steps[qi].querySelector("input").focus(); });
    back.addEventListener("click", function () { showStep(qi - 1); });
    quiz.addEventListener("change", function () {
      qErr.hidden = true;
      if (qi < steps.length - 1) setTimeout(function () { showStep(qi + 1); }, 260);
    });
    showStep(0);

    var SECOND = { shop: ["system", "web"], food: ["ai", "web"], services: ["web", "ai"], clinic: ["system", "ai"], factory: ["system", "support"], online: ["web", "ai"] };
    var PRIMARY = { online: "web", messages: "ai", stock: "system", it: "support", unsure: "consult" };
    var SIZE = {
      s: ["حل بسيط وسهل يناسب فريق صغير", "a simple setup that suits a small team"],
      m: ["مع حسابات وصلاحيات لكل فرد في الفريق", "with accounts and permissions for each team member"],
      l: ["مع صلاحيات للفريق وتقارير للإدارة", "with team permissions and management reports"],
      xl: ["مع تدريب للفريق ودعم فني مستمر", "with team training and ongoing support"]
    };
    var PRIORITY = {
      fast: ["نبدأ بنسخة أولى بسيطة تشتغل بسرعة، ونطوّر عليها بعد كده.", "We launch a simple first version quickly, then improve it."],
      budget: ["نبدأ بالأهم بس، وباقي الخطوات على مراحل حسب ميزانيتك.", "We start with what matters most and phase the rest to fit your budget."],
      scale: ["نبني على أساس قوي يكبر معاك: ربط كل الأدوات ببعض وتقارير شاملة.", "We build a strong base that grows with you: connected tools and full reports."]
    };
    function label(name) {
      var c = quiz.querySelector('input[name="' + name + '"]:checked');
      return c ? c.nextElementSibling.textContent : "";
    }
    quiz.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!answered(qi)) return needAnswer();
      var a = {};
      ["business", "size", "challenge", "priority"].forEach(function (n) {
        var c = quiz.querySelector('input[name="' + n + '"]:checked'); a[n] = c ? c.value : "";
      });
      var first = PRIMARY[a.challenge] || "consult";
      var second = (SECOND[a.business] || ["web", "ai"]).filter(function (k) { return k !== first; })[0];
      var en = lang() === "en";
      function stepHTML(k, extra) {
        return "<li><div><strong>" + SV[k][en ? "en" : "ar"] + "</strong><span>" + (en ? "Why: " : "ليه؟ ") + SV[k][en ? "wen" : "war"] + (extra ? " " + extra : "") + "</span></div></li>";
      }
      var sizeTxt = SIZE[a.size] ? SIZE[a.size][en ? 1 : 0] : "";
      var prioTxt = PRIORITY[a.priority] ? PRIORITY[a.priority][en ? 1 : 0] : "";
      var summary = (en ? "Hello Sana, I took the quiz on your website:\n" : "أهلًا سنآ، عملت اختبار \"اعرف حلّك\" على الموقع:\n") +
        "- " + label("business") + "\n- " + label("size") + "\n- " + label("challenge") + "\n- " + label("priority") + "\n" +
        (en ? "Suggested: " : "الخطة المقترحة: ") + SV[first][en ? "en" : "ar"] + " + " + SV[second][en ? "en" : "ar"];
      result.innerHTML =
        "<h3>" + (en ? "Your suggested plan" : "خطتك المقترحة") + " ✦</h3>" +
        "<p>" + (en ? "For a " : "لنشاط ") + "<strong>" + label("business") + "</strong>" + (en ? " with a team of " : " بفريق ") + label("size") + (en ? " people" : "") + ":</p>" +
        '<ol class="plan-steps">' + stepHTML(first, sizeTxt ? "(" + sizeTxt + ")" : "") + stepHTML(second) +
        "<li><div><strong>" + (en ? "How we start" : "هنبدأ إزاي") + "</strong><span>" + prioTxt + "</span></div></li></ol>" +
        '<div class="plan-actions">' +
        '<a class="btn btn-primary" target="_blank" rel="noopener" href="' + waLink(summary) + '">' + (en ? "Send my plan on WhatsApp" : "ابعت خطتي على واتساب") + "</a>" +
        '<button class="btn btn-ghost" type="button" data-plan="chat">' + (en ? "Ask Sana Assistant" : "اسأل مساعد سنآ") + "</button>" +
        '<button class="btn btn-ghost" type="button" data-plan="again">' + (en ? "Start over" : "ابدأ من جديد") + "</button></div>";
      result.dataset.summary = summary;
      quiz.hidden = true; bar.parentNode.hidden = true; result.hidden = false; result.focus();
    });
    result.addEventListener("click", function (e) {
      var b = e.target.closest("[data-plan]"); if (!b) return;
      if (b.dataset.plan === "again") {
        quiz.reset(); quiz.hidden = false; bar.parentNode.hidden = false; result.hidden = true; showStep(0);
        steps[0].querySelector("input").focus();
      } else if (window.SanaChat) {
        window.SanaChat.open(result.dataset.summary);
      }
    });
  }

  /* ===== Sana Assistant (chat) ===== */
  var fab = $(".chat-fab"), chat = document.getElementById("chat");
  if (fab && chat) {
    var log = $(".chat-log", chat), chips = $(".chat-chips", chat), cform = $(".chat-form", chat);
    var input = document.getElementById("chat-input"), waBtn = $(".chat-wa", chat);
    var history = [], userLines = [], started = false, busy = false;

    function addMsg(role, text) {
      var d = document.createElement("div");
      d.className = "msg " + role; d.textContent = text;
      log.appendChild(d); log.scrollTop = log.scrollHeight;
      return d;
    }
    function setChips(list) {
      chips.innerHTML = "";
      list.forEach(function (c) {
        var el;
        if (c.href) { el = document.createElement("a"); el.href = c.href; el.target = "_blank"; el.rel = "noopener"; }
        else { el = document.createElement("button"); el.type = "button"; el.addEventListener("click", function () { c.run(); }); }
        el.className = "chip"; el.textContent = c.label;
        chips.appendChild(el);
      });
    }
    function updateWa() {
      var t = L("أهلًا سنآ، كنت بكلّم المساعد على الموقع:\n", "Hello Sana, I was chatting with the website assistant:\n") + userLines.slice(-4).join("\n");
      waBtn.href = waLink(userLines.length ? t : L("أهلًا سنآ، عايز أستفسر عن خدماتكم.", "Hello Sana, I would like to ask about your services."));
    }
    function serviceChips() {
      var list = SV_ORDER.map(function (k) {
        return { label: SV[k][lang()], run: function () { userSays(SV[k][lang()], k); } };
      });
      list.push({ label: L("مش متأكد", "Not sure"), run: function () { userSays(L("مش متأكد محتاج إيه", "I'm not sure what I need"), "unsure"); } });
      setChips(list);
    }
    function scriptedReply(text, forced) {
      var k = forced || matchService(text), n = norm(text);
      if (!forced && /(سعر|بكام|تكلفه|اسعار|price|cost|how much)/.test(n)) {
        botSays(L("الأسعار بتتحدد حسب احتياجك بالظبط. ابعتلنا تفاصيل بسيطة على واتساب وفريقنا يرد عليك بعرض واضح.",
          "Pricing depends on exactly what you need. Send us a few details on WhatsApp and our team will reply with a clear quote."));
        return setChips([{ label: L("ابعت على واتساب", "Send on WhatsApp"), href: waBtn.href }, { label: L("اعرض الخدمات", "Show services"), run: serviceChips }]);
      }
      if (k === "unsure") {
        botSays(L("ولا يهمك! جرّب اختبار \"اعرف حلّك\": 4 أسئلة سريعة وتطلعلك خطة مقترحة. أو قولّي باختصار شغلك إيه وإيه اللي تاعبك.",
          "No problem! Try the \"Find your solution\" quiz: four quick questions and you get a suggested plan. Or tell me briefly about your business and what is bothering you."));
        return setChips([{ label: L("افتح الاختبار", "Open the quiz"), run: function () { window.location.href = "index.html#plan"; } }, { label: L("اعرض الخدمات", "Show services"), run: serviceChips }]);
      }
      if (k && SV[k]) {
        botSays(SV[k][lang() === "en" ? "den" : "dar"] + "\n" + L("تحب نكمّل على واتساب ونفهم احتياجك بالتفصيل؟", "Shall we continue on WhatsApp to understand your needs in detail?"));
        return setChips([
          { label: L("اطلب الخدمة دي على واتساب", "Request this on WhatsApp"), href: waLink(L("أهلًا سنآ، مهتم بخدمة: ", "Hello Sana, I'm interested in: ") + SV[k][lang()] + (userLines.length ? "\n" + userLines.slice(-3).join("\n") : "")) },
          { label: L("خدمة تانية", "Another service"), run: serviceChips }
        ]);
      }
      botSays(L("تمام! علشان أفهمك أكتر، اختار أقرب حاجة لاحتياجك:", "Got it! To understand you better, pick what is closest to your need:"));
      serviceChips();
    }
    function botSays(text) { addMsg("bot", text); history.push({ role: "assistant", content: text }); }

    function userSays(text, forcedKey) {
      if (busy || !text) return;
      addMsg("user", text);
      userLines.push(text); updateWa();
      chips.innerHTML = "";
      if (history.length && history[history.length - 1].role === "user") history.pop();
      history.push({ role: "user", content: text });
      if (!CONFIG.chatEndpoint || forcedKey) { scriptedReply(text, forcedKey); return; }

      busy = true;
      var typing = addMsg("bot typing", "…");
      fetch(CONFIG.chatEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lang: lang(), messages: history.filter(function (m, i) { return i > 0 || m.role === "user"; }) })
      }).then(function (r) { return r.json().catch(function () { return {}; }); })
        .then(function (data) {
          typing.remove();
          if (data && data.reply) {
            botSays(data.reply);
            setChips([{ label: L("كمّل على واتساب", "Continue on WhatsApp"), href: waBtn.href }]);
          } else {
            scriptedReply(text);
          }
        })
        .catch(function () { typing.remove(); scriptedReply(text); })
        .then(function () { busy = false; });
    }

    function openChat(prefill) {
      chat.hidden = false; fab.setAttribute("aria-expanded", "true");
      if (!started) {
        started = true;
        var hello = L("أهلًا! أنا مساعد سنآ ✦\nقولّي شغلك إيه ومحتاج إيه، أو اختار من الخدمات دي:",
          "Hi! I'm Sana Assistant ✦\nTell me about your business and what you need, or pick a service:");
        addMsg("bot", hello);
        serviceChips(); updateWa();
      }
      if (prefill) userSays(prefill);
      input.focus();
    }
    function closeChat() { chat.hidden = true; fab.setAttribute("aria-expanded", "false"); fab.focus(); }
    fab.addEventListener("click", function () { openChat(); });
    $(".chat-close", chat).addEventListener("click", closeChat);
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      if (!chat.hidden) closeChat();
      else if (nav && nav.classList.contains("open")) { nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.focus(); }
    });
    cform.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = input.value.trim(); if (!v) return;
      input.value = ""; userSays(v.slice(0, 1200));
    });
    window.SanaChat = { open: openChat };
  }

  /* ===== Easter egg: tap the ✦ five times ===== */
  var taps = 0, lastTap = 0;
  function burst(x, y) {
    if (reduceMotion) return;
    for (var i = 0; i < 22; i++) {
      var s = document.createElement("span");
      var ang = Math.random() * Math.PI * 2, dist = 80 + Math.random() * 160;
      s.className = "burst"; s.textContent = "✦";
      s.style.left = x + "px"; s.style.top = y + "px";
      s.style.setProperty("--x", Math.cos(ang) * dist + "px");
      s.style.setProperty("--y", Math.sin(ang) * dist + "px");
      s.style.setProperty("--rot", (Math.random() * 540 - 270) + "deg");
      s.style.setProperty("--s", (0.8 + Math.random() * 1.4) + "rem");
      document.body.appendChild(s);
      setTimeout(function (el) { el.remove(); }, 1200, s);
    }
  }
  var toast = $(".toast"), toastTimer;
  function showToast(html) {
    if (!toast) return;
    toast.innerHTML = html; toast.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toast.hidden = true; }, 7000);
  }
  $$(".egg, .egg-target").forEach(function (el) {
    el.addEventListener("click", function (e) {
      var now = Date.now();
      taps = now - lastTap < 2500 ? taps + 1 : 1; lastTap = now;
      if (taps < 5) return;
      taps = 0;
      var r = el.getBoundingClientRect();
      burst(e.clientX || r.left + r.width / 2, e.clientY || r.top + r.height / 2);
      showToast(L("✦ لقيت نجمة سنآ السرية! الفضول ده بالظبط اللي بيصنع المبدعين. ", "✦ You found Sana's secret star! That curiosity is exactly what makes great builders. ") +
        '<a href="careers.html">' + L("انضم لفريقنا", "Join our team") + "</a>");
    });
  });
})();
