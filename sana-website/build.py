#!/usr/bin/env python3
"""Build the Sana Technology static site: python3 build.py -> ./site"""
import html, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
SITE_URL = "https://sanatechgroup.online"
PHONE_DISPLAY = "01503331435"
PHONE_TEL = "+201503331435"
WHATSAPP = "201503331435"

def e(s):
    return html.escape(s, quote=True)

def t(tag, ar, en, attrs=""):
    """Bilingual element: Arabic shown by default, English swapped in by script.js."""
    a = f" {attrs}" if attrs else ""
    return f'<{tag}{a} data-ar="{e(ar)}" data-en="{e(en)}">{e(ar)}</{tag}>'

NAV = [
    ("index.html", "الرئيسية", "Home"),
    ("about.html", "من نحن", "About"),
    ("services.html", "خدماتنا", "Services"),
    ("work.html", "أعمالنا", "Our work"),
    ("store.html", "متجرنا", "Store"),
    ("news.html", "أخبار التقنية", "Tech news"),
    ("careers.html", "الوظائف", "Careers"),
    ("contact.html", "تواصل معنا", "Contact"),
]

ICONS = {
    "web": '<path d="M3 5h18v14H3z"/><path d="M3 9h18M7 7h.01M10 7h.01"/>',
    "mobile": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    "system": '<path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4z"/><path d="M16.5 13v7M13 16.5h7"/>',
    "ai": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "support": '<path d="M4 14v-2a8 8 0 0116 0v2"/><rect x="2" y="14" width="5" height="6" rx="2"/><rect x="17" y="14" width="5" height="6" rx="2"/>',
    "consult": '<path d="M3 20l5-6 4 3 8-10"/><path d="M14 7h6v6"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 17h6"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "simple": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "fit": '<path d="M12 3v18M3 12h18"/><circle cx="12" cy="12" r="4"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0114 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 006 6L16 13l5 2v4a2 2 0 01-2 2A17 17 0 013 5a2 2 0 012-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "moon": '<path d="M20 14.5A8 8 0 019.5 4a8 8 0 1010.5 10.5z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "send": '<path d="M4 12l16-8-6 16-2.5-6.5z"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "news": '<path d="M4 5h13v14H6a2 2 0 01-2-2z"/><path d="M17 8h3v9a2 2 0 01-2 2"/><path d="M7 9h7M7 12h7M7 15h4"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5"/>',
    "chat": '<path d="M21 12a8 8 0 01-11.6 7.1L4 20l1-4.6A8 8 0 1121 12z"/>',
}

def icon(name):
    return (f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')

SERVICES = [
    ("web", "المواقع والمتاجر الإلكترونية", "Websites & online stores",
     "مواقع سريعة واحترافية ومتاجر جاهزة للبيع أونلاين، بتشتغل كويس على الموبايل.",
     "Fast, professional websites and ready-to-sell online stores that work great on mobile.",
     [("مواقع شركات وصفحات هبوط", "Company sites & landing pages"),
      ("متاجر إلكترونية ودفع أونلاين", "E-commerce & online payments"),
      ("استضافة ودومين وإيميلات رسمية", "Hosting, domains & business email")]),
    ("mobile", "تطبيقات الموبايل", "Mobile apps",
     "تطبيقات Android و iOS بتجربة استخدام بسيطة لعملائك وفريقك.",
     "Android and iOS apps with a simple experience for your customers and team.",
     [("تطبيقات للعملاء والطلبات", "Customer & ordering apps"),
      ("تطبيقات داخلية للموظفين", "Internal staff apps"),
      ("ربط مع أنظمتك الحالية", "Integration with your systems")]),
    ("system", "أنظمة إدارة الأعمال", "Business systems",
     "أنظمة تنظّم شغلك: مبيعات، مخازن، حسابات، وعملاء — في مكان واحد.",
     "Systems that organise your work — sales, inventory, accounts and customers in one place.",
     [("أنظمة ERP و CRM", "ERP & CRM"),
      ("نقاط بيع POS", "Point of sale (POS)"),
      ("لوحات تقارير ومتابعة", "Reports & dashboards")]),
    ("ai", "الذكاء الاصطناعي والبوتات", "AI & chatbots",
     "مساعدين أذكياء وبوتات بترد على عملائك وتنجز المهام المتكررة بدالك.",
     "Smart assistants and bots that answer customers and handle repetitive tasks for you.",
     [("AI Agents للشركات", "AI agents for business"),
      ("بوتات واتساب وماسنجر", "WhatsApp & Messenger bots"),
      ("أتمتة المهام المتكررة", "Workflow automation")]),
    ("support", "الدعم الفني والشبكات", "IT support & networks",
     "تركيب وصيانة الأجهزة والشبكات وكاميرات المراقبة، ودعم فني تقدر تعتمد عليه.",
     "Installation and maintenance of devices, networks and CCTV, with support you can rely on.",
     [("تأسيس وصيانة الشبكات", "Network setup & maintenance"),
      ("كاميرات مراقبة وأنظمة أمان", "CCTV & security systems"),
      ("صيانة أجهزة ودعم فني", "Device repair & IT support")]),
    ("consult", "الاستشارات والتحول الرقمي", "Consulting & digital transformation",
     "نساعدك تختار التقنية الصح لشغلك ونمشي معاك خطوة بخطوة.",
     "We help you pick the right technology for your business and guide you step by step.",
     [("تحليل احتياجات شغلك", "Business needs analysis"),
      ("خطة تحول رقمي واضحة", "A clear digital roadmap"),
      ("تدريب فريقك", "Team training")]),
]

PRODUCTS = [
    ("system", "نظام سنآ", "Sana System",
     "نظام متكامل لإدارة شركتك: مبيعات، مخازن، فواتير، وتقارير.",
     "An all-in-one system to run your company: sales, inventory, invoices and reports."),
    ("ai", "Sana AI Agent", "Sana AI Agent",
     "موظف ذكي بيشتغل 24 ساعة: يرد على العملاء، ينظم الطلبات، ويساعد فريقك.",
     "A smart assistant working around the clock: answers customers, organises orders, helps your team."),
    ("bot", "بوتات سنآ", "Sana Bots",
     "بوتات جاهزة لواتساب والسوشيال ميديا تبدأ تشتغل في دقائق.",
     "Ready-made bots for WhatsApp and social media, up and running in minutes."),
]


CUR = ' aria-current="page"'


def header(active):
    links = "\n".join(
        f'        <a href="{href}"{CUR if href == active else ""} '
        f'data-ar="{ar}" data-en="{en}">{ar}</a>'
        for href, ar, en in NAV[1:-1])
    return f'''<a class="skip-link" href="#main" data-ar="تخطَّ إلى المحتوى" data-en="Skip to content">تخطَّ إلى المحتوى</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Sana Technology">
      <img class="logo-light-bg" src="assets/logo.png" alt="Sana Technology" width="146" height="44">
      <img class="logo-dark-bg" src="assets/logo-light.png" alt="Sana Technology" width="146" height="44">
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="visually-hidden" data-ar="القائمة" data-en="Menu">القائمة</span><span class="menu-bar" aria-hidden="true"></span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
{links}
      <div class="nav-tools">
        <button class="theme-toggle" type="button" aria-pressed="false" aria-label="الوضع الليلي / Dark mode">{icon("moon")}{icon("sun")}</button>
        <button class="lang-toggle" type="button" data-ar="EN" data-en="ع" aria-label="Switch language">EN</button>
      </div>
      <a class="btn btn-primary btn-sm" href="contact.html"{CUR if active == "contact.html" else ""} data-ar="تواصل معنا" data-en="Contact us">تواصل معنا</a>
    </nav>
  </div>
</header>'''


def footer():
    links = "".join(f'<li><a href="{h}" data-ar="{ar}" data-en="{en}">{ar}</a></li>' for h, ar, en in NAV)
    svc = "".join(f'<li><a href="services.html#{k}" data-ar="{e(ar)}" data-en="{e(en)}">{e(ar)}</a></li>'
                  for k, ar, en, *_ in SERVICES[:4])
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <p class="footer-brand">Sana <button class="egg" type="button" aria-label="✦">✦</button><span>Technology</span></p>
      {t("p", "تقنية تسبق الزمن — بنسهّل التكنولوجيا ونقدّمها لأي حد.", "Tech Beyond Time — making technology simple and available to everyone.", 'class="footer-tag"')}
    </div>
    <nav aria-label="Footer">
      {t("h2", "روابط", "Links")}
      <ul>{links}</ul>
    </nav>
    <div>
      {t("h2", "خدماتنا", "Services")}
      <ul>{svc}</ul>
    </div>
    <div>
      {t("h2", "تواصل", "Get in touch")}
      <ul>
        <li>{t("span", "مدينة الشروق، القاهرة الجديدة", "El Shorouk City, New Cairo")}</li>
        <li><a href="tel:{PHONE_TEL}"><bdi dir="ltr">{PHONE_DISPLAY}</bdi></a></li>
        <li><a href="https://wa.me/{WHATSAPP}" rel="noopener" data-ar="واتساب" data-en="WhatsApp">واتساب</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© <span id="year">2026</span> Sana Technology. {t("span", "جميع الحقوق محفوظة.", "All rights reserved.")}</p>
  </div>
</footer>'''


def page(filename, title_ar, title_en, desc, body):
    title = f"{title_en} | Sana Technology" if filename != "index.html" else "Sana Technology | Tech Beyond Time"
    # Cloudflare Pages serves /about.html at /about, so canonical URLs drop ".html"
    canonical = SITE_URL + "/" + ("" if filename == "index.html" else filename[:-5])
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#fcfaff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#120c1f" media="(prefers-color-scheme: dark)">
  <script>(function(){{try{{var t=localStorage.getItem("sana-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}}})();</script>
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Sana Technology">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE_URL}/assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Sana Technology","alternateName":"سنآ","url":"{SITE_URL}","logo":"{SITE_URL}/assets/logo.png","telephone":"{PHONE_TEL}","address":{{"@type":"PostalAddress","addressLocality":"El Shorouk City","addressRegion":"Cairo","addressCountry":"EG"}}}}</script>
</head>
<body data-page="{filename}">
<div class="scroll-progress" aria-hidden="true"></div>
{header(filename)}
<main id="main">
{body}
</main>
{footer()}
{chat_widget()}
<div class="toast" role="status" hidden></div>
<script src="script.js" defer></script>
</body>
</html>
'''


def page_hero(kicker_ar, kicker_en, h_ar, h_en, p_ar, p_en):
    return f'''<section class="page-hero">
  <div class="container">
    {t("p", kicker_ar, kicker_en, 'class="kicker"')}
    {t("h1", h_ar, h_en)}
    {t("p", p_ar, p_en, 'class="lead"')}
  </div>
</section>'''


def cta_band():
    return f'''<section class="section">
  <div class="container">
    <div class="cta-band">
      <div>
        {t("h2", "عندك فكرة أو مشكلة تقنية؟", "Got an idea or a tech problem?")}
        {t("p", "كلّمنا ونرشّحلك الحل المناسب لشغلك وميزانيتك.", "Talk to us and we will suggest the right solution for your business and budget.")}
      </div>
      {t("a", "ابدأ معنا", "Start with us", 'class="btn btn-light" href="contact.html"')}
    </div>
  </div>
</section>'''


def service_cards(link=True):
    out = []
    for k, ar, en, dar, den, _ in SERVICES:
        more = t("a", "اعرف أكتر", "Learn more", f'class="card-link" href="services.html#{k}"') if link else ""
        out.append(f'''<article class="card">
        <div class="card-icon">{icon(k)}</div>
        {t("h3", ar, en)}
        {t("p", dar, den)}
        {more}
      </article>''')
    return "\n      ".join(out)


def product_cards():
    return "\n      ".join(f'''<article class="card product">
        <span class="badge" data-ar="قريبًا" data-en="Coming soon">قريبًا</span>
        <div class="card-icon">{icon(k)}</div>
        {t("h3", ar, en)}
        {t("p", dar, den)}
      </article>''' for k, ar, en, dar, den in PRODUCTS)


def field(fid, name, ar, en, kind="input", extra=""):
    label = t("label", ar, en, f'for="{fid}"')
    if kind == "textarea":
        ctl = f'<textarea id="{fid}" name="{name}" rows="5" required></textarea>'
    elif kind == "select":
        ctl = f'<select id="{fid}" name="{name}" required>{extra}</select>'
    else:
        ctl = f'<input id="{fid}" name="{name}" {extra} required>'
    return f'<div class="field">{label}{ctl}</div>'


def options(pairs):
    first = '<option value="" data-ar="اختر…" data-en="Choose…">اختر…</option>'
    return first + "".join(f'<option value="{e(en)}" data-ar="{e(ar)}" data-en="{e(en)}">{e(ar)}</option>' for ar, en in pairs)


def form(form_id, kind, fields, submit_ar, submit_en):
    return f'''<form class="form" id="{form_id}" data-kind="{kind}" novalidate>
        {"".join(fields)}
        <p class="form-msg" role="status" hidden></p>
        {t("button", submit_ar, submit_en, 'class="btn btn-primary" type="submit"')}
      </form>'''



def chat_widget():
    return f'''<button class="chat-fab" type="button" aria-controls="chat" aria-expanded="false">
  {icon("chat")}<span data-ar="اسأل مساعد سنآ" data-en="Ask Sana Assistant">اسأل مساعد سنآ</span>
</button>
<section class="chat" id="chat" hidden aria-labelledby="chat-title">
  <div class="chat-head">
    <div>
      <p class="chat-title" id="chat-title"><span data-ar="مساعد سنآ" data-en="Sana Assistant">مساعد سنآ</span> <span aria-hidden="true">✦</span></p>
      <p class="chat-sub" data-ar="قولّي محتاج إيه وأنا أرشّحلك الحل" data-en="Tell me what you need and I will suggest a solution">قولّي محتاج إيه وأنا أرشّحلك الحل</p>
    </div>
    <button class="chat-close" type="button" aria-label="إغلاق / Close">{icon("close")}</button>
  </div>
  <div class="chat-log" role="log" aria-live="polite"></div>
  <div class="chat-chips"></div>
  <form class="chat-form">
    <label class="visually-hidden" for="chat-input" data-ar="رسالتك" data-en="Your message">رسالتك</label>
    <input id="chat-input" name="message" autocomplete="off" maxlength="1200" data-ph-ar="اكتب سؤالك هنا…" data-ph-en="Type your question…" placeholder="اكتب سؤالك هنا…">
    <button class="chat-send" type="submit" aria-label="إرسال / Send">{icon("send")}</button>
  </form>
  <a class="chat-wa" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" data-ar="كمّل المحادثة على واتساب" data-en="Continue on WhatsApp">كمّل المحادثة على واتساب</a>
</section>'''


QUIZ = [
    ("business", "نوع نشاطك إيه؟", "What kind of business do you run?", [
        ("shop", "محل أو تجارة", "Shop or trading"), ("food", "مطعم أو كافيه", "Restaurant or café"),
        ("services", "شركة خدمات", "Service company"), ("clinic", "عيادة أو مركز طبي", "Clinic or medical center"),
        ("factory", "مصنع أو مخزن", "Factory or warehouse"), ("online", "بيزنس أونلاين أو براند", "Online business or brand")]),
    ("size", "فريقك كام شخص؟", "How big is your team?", [
        ("s", "1 – 5", "1 – 5"), ("m", "6 – 20", "6 – 20"), ("l", "21 – 50", "21 – 50"), ("xl", "أكتر من 50", "More than 50")]),
    ("challenge", "إيه أكبر تحدي عندك دلوقتي؟", "What is your biggest challenge right now?", [
        ("online", "مفيش وجود أونلاين والعملاء قليلين", "No online presence, too few customers"),
        ("messages", "الرسايل والطلبات كتير ومش ملحقين", "Too many messages and orders to keep up"),
        ("stock", "المخزون والحسابات ملخبطة", "Inventory and accounts are a mess"),
        ("it", "الأجهزة أو الشبكة بتقع كتير", "Devices or the network keep failing"),
        ("unsure", "مش عارف أبدأ منين", "Not sure where to start")]),
    ("priority", "إيه الأهم ليك؟", "What matters most to you?", [
        ("fast", "أسرع حل", "The fastest fix"), ("budget", "أوفر حل", "The most affordable option"),
        ("scale", "حل قوي يكبر معايا", "A strong solution that grows with me")]),
]


def quiz_section():
    steps = []
    for i, (name, qar, qen, opts) in enumerate(QUIZ):
        radios = "".join(
            f'<label class="opt"><input type="radio" name="{name}" value="{v}" required><span data-ar="{e(a)}" data-en="{e(b)}">{e(a)}</span></label>'
            for v, a, b in opts)
        steps.append(f'''<fieldset class="quiz-step" data-step="{i}">
          <legend><span class="quiz-count">{i + 1} / {len(QUIZ)}</span> <span data-ar="{e(qar)}" data-en="{e(qen)}">{e(qar)}</span></legend>
          <div class="opts">{radios}</div>
        </fieldset>''')
    return f'''<section class="section section-soft" id="plan">
  <div class="container">
    <div class="section-head">
      {t("p", "اعرف حلّك", "Find your solution", 'class="kicker"')}
      {t("h2", "اعرف حلّك التقني في 60 ثانية", "Find your tech solution in 60 seconds")}
      {t("p", "4 أسئلة سريعة، وفي الآخر هتطلعلك خطة مقترحة تناسب شغلك.", "Four quick questions, then you get a suggested plan for your business.", 'class="section-sub"')}
    </div>
    <div class="quiz">
      <div class="quiz-bar" aria-hidden="true"><span></span></div>
      <form id="quiz-form" novalidate>
        {"".join(steps)}
        <div class="quiz-nav">
          {t("button", "السابق", "Back", 'class="btn btn-ghost btn-sm" type="button" data-quiz="back"')}
          {t("button", "التالي", "Next", 'class="btn btn-primary btn-sm" type="button" data-quiz="next"')}
          {t("button", "اعرض خطتي", "Show my plan", 'class="btn btn-primary btn-sm" type="submit" data-quiz="done"')}
        </div>
        <p class="form-msg error" role="alert" hidden></p>
      </form>
      <div class="quiz-result" tabindex="-1" hidden></div>
    </div>
  </div>
</section>'''


def before_after_section():
    before = [("دفتر طلبات بخط الإيد", "Orders written in a notebook"),
              ("شيت Excel بـ 5 نسخ مختلفة", "An Excel sheet in 5 different versions"),
              ("37 رسالة واتساب مستنية رد", "37 WhatsApp messages waiting for a reply"),
              ("جرد المخزن بالإيد كل أسبوع", "Counting stock by hand every week"),
              ("مش عارف كسبت كام الشهر ده", "No idea how much you earned this month")]
    notes = "".join(f'<li class="note n{i}" data-ar="{e(a)}" data-en="{e(b)}">{e(a)}</li>' for i, (a, b) in enumerate(before))
    bars = "".join(f'<span style="--h:{h}%"></span>' for h in (42, 58, 51, 70, 64, 86, 78))
    return f'''<section class="section" id="before-after">
  <div class="container">
    <div class="section-head">
      {t("p", "قبل وبعد", "Before & after", 'class="kicker"')}
      {t("h2", "شوف الفرق بنفسك", "See the difference yourself")}
      {t("p", "اسحب الخط يمين وشمال علشان تقارن شغلك قبل سنآ وبعدها.", "Drag the line left and right to compare your work before and after Sana.", 'class="section-sub"')}
    </div>
    <div class="ba" style="--pos:50%">
      <div class="ba-pane ba-before">
        {t("p", "قبل سنآ", "Before Sana", 'class="ba-label"')}
        <ul class="notes">{notes}</ul>
      </div>
      <div class="ba-pane ba-after">
        {t("p", "بعد سنآ", "With Sana", 'class="ba-label"')}
        <div class="dash">
          <div class="kpi"><span data-ar="طلبات النهارده" data-en="Orders today">طلبات النهارده</span><strong>48</strong></div>
          <div class="kpi"><span data-ar="وقت الرد" data-en="Reply time">وقت الرد</span><strong data-ar="أقل من دقيقة" data-en="Under a minute">أقل من دقيقة</strong></div>
          <div class="kpi"><span data-ar="المخزون" data-en="Inventory">المخزون</span><strong data-ar="محدّث لحظيًا" data-en="Live">محدّث لحظيًا</strong></div>
          <div class="chart"><span class="chart-label" data-ar="مبيعات الأسبوع" data-en="This week's sales">مبيعات الأسبوع</span><div class="bars">{bars}</div></div>
        </div>
      </div>
      <div class="ba-handle" aria-hidden="true"><span>⟷</span></div>
      <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="قارن قبل وبعد / Compare before and after">
    </div>
    {t("p", "مثال توضيحي لشكل الشغل بعد نظام إدارة وبوت رد آلي.", "Illustrative example of work after a management system and an auto-reply bot.", 'class="ba-note"')}
  </div>
</section>'''


def calc_field(fid, ar, en, lo, hi, step, val, unit_ar, unit_en):
    return f'''<div class="calc-field">
        <label for="{fid}"><span data-ar="{e(ar)}" data-en="{e(en)}">{e(ar)}</span>
          <output for="{fid}" class="calc-val"><bdi>{val}</bdi> <span data-ar="{e(unit_ar)}" data-en="{e(unit_en)}">{e(unit_ar)}</span></output></label>
        <input id="{fid}" type="range" min="{lo}" max="{hi}" step="{step}" value="{val}">
      </div>'''


def calculator_section():
    return f'''<section class="section section-soft" id="calculator">
  <div class="container">
    <div class="section-head">
      {t("p", "حاسبة التوفير", "Savings calculator", 'class="kicker"')}
      {t("h2", "احسب هتوفّر كام مع الأتمتة", "See what automation could save you")}
      {t("p", "حرّك الأرقام حسب شغلك، والحاسبة هتطلعلك تقدير للوقت والفلوس اللي بتضيع في الشغل اليدوي المتكرر.", "Adjust the numbers to match your business and get an estimate of the time and money lost to repetitive manual work.", 'class="section-sub"')}
    </div>
    <div class="calc">
      <form class="calc-inputs" id="calc-form" onsubmit="return false">
        {calc_field("calc-emp", "عدد الموظفين اللي بيعملوا شغل متكرر", "Employees doing repetitive work", 1, 100, 1, 5, "موظف", "people")}
        {calc_field("calc-hours", "ساعات الشغل المتكرر لكل موظف في اليوم", "Repetitive hours per employee per day", 0.5, 8, 0.5, 3, "ساعة", "hours")}
        {calc_field("calc-salary", "متوسط المرتب الشهري", "Average monthly salary", 3000, 60000, 500, 10000, "جنيه", "EGP")}
      </form>
      <div class="calc-out" aria-live="polite">
        <div class="stat"><span data-ar="ساعات بتتوفّر في الشهر" data-en="Hours saved per month">ساعات بتتوفّر في الشهر</span><strong id="out-hours">156</strong></div>
        <div class="stat"><span data-ar="توفير شهري تقريبي" data-en="Approx. monthly saving">توفير شهري تقريبي</span><strong id="out-month">8,864</strong></div>
        <div class="stat stat-main"><span data-ar="توفير في السنة" data-en="Saving per year">توفير في السنة</span><strong id="out-year">106,364</strong></div>
        {t("p", "تقدير تقريبي: بنفترض 26 يوم شغل في الشهر، و176 ساعة شغل للموظف، وإن الأتمتة بتوفّر حوالي 40% من الوقت المتكرر. الأرقام الحقيقية بتختلف حسب نشاطك.", "Rough estimate: assumes 26 working days a month, 176 working hours per employee, and that automation saves about 40% of repetitive time. Real numbers depend on your business.", 'class="calc-note"')}
        {t("a", "اطلب خطة أتمتة لشغلك", "Get an automation plan", 'class="btn btn-primary" href="contact.html?service=system"')}
      </div>
    </div>
  </div>
</section>'''


# Keep in sync with worker/src/news.js (FEEDS)
NEWS_SOURCES = [
    ("MIT Technology Review", "https://www.technologyreview.com"), ("The Verge", "https://www.theverge.com"),
    ("TechCrunch", "https://techcrunch.com"), ("Ars Technica", "https://arstechnica.com"), ("WIRED", "https://www.wired.com"),
    ("IEEE Spectrum", "https://spectrum.ieee.org"), ("BBC News", "https://www.bbc.com/news/technology"),
    ("BBC عربي", "https://www.bbc.com/arabic/science-and-tech"), ("البوابة العربية للأخبار التقنية", "https://aitnews.com"),
    ("عالم التقنية", "https://www.tech-wd.com"),
]


def news_body():
    filters = [("all", "الكل", "All"), ("ai", "الذكاء الاصطناعي", "AI"), ("ar", "بالعربي", "Arabic"), ("en", "بالإنجليزي", "English")]
    btns = "".join(f'<button class="nf" type="button" data-filter="{k}" aria-pressed="{str(k == "all").lower()}" data-ar="{e(a)}" data-en="{e(b)}">{e(a)}</button>' for k, a, b in filters)
    skeleton = "".join('<article class="news-card skeleton" aria-hidden="true"><div class="nc-img"></div><div class="nc-body"><span></span><span></span><span></span></div></article>' for _ in range(6))
    srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{e(n)}</a></li>' for n, u in NEWS_SOURCES)
    return page_hero("أخبار التقنية", "Tech news", "آخر أخبار التكنولوجيا والذكاء الاصطناعي", "The latest in tech and AI",
                     "أهم الأخبار من مصادر عالمية وعربية موثوقة، بتتحدّث لوحدها كل ربع ساعة. كل خبر معاه رابط المصدر الأصلي.",
                     "Top stories from trusted global and Arabic outlets, refreshed automatically every 15 minutes. Every story links to its original source.") + f'''
<section class="section news-section">
  <div class="container">
    <div class="news-bar">
      <div class="news-filters" role="group" aria-label="فلترة الأخبار / Filter news">{btns}</div>
      <p class="news-updated" aria-live="polite"></p>
    </div>
    <div class="news-grid" id="news-grid" aria-busy="true">{skeleton}</div>
    <p class="news-empty" hidden></p>
    <div class="news-sources">
      {t("h2", "مصادرنا", "Our sources")}
      <ul>{srcs}</ul>
      {t("p", "بنعرض عنوان الخبر وملخص قصير بس، والخبر كامل عند مصدره. حقوق الأخبار لأصحابها.", "We show only the headline and a short summary; the full story lives with its source. All rights belong to the publishers.", 'class="muted"')}
    </div>
  </div>
</section>'''

# ---------------- Pages ----------------

home = f'''<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      {t("p", "شركة تكنولوجيا بإدارة كويتية · مدينة الشروق", "Kuwaiti-managed tech company · El Shorouk City", 'class="kicker"')}
      <h1><span data-ar="تقنية تسبق" data-en="Tech beyond">تقنية تسبق</span> <span class="grad" data-ar="الزمن" data-en="time">الزمن</span></h1>
      {t("p", "في سنآ بنسهّل التكنولوجيا ونقدّمها لأي حد — من الفكرة، للتنفيذ، للتشغيل والدعم.", "At Sana we make technology simple and bring it to everyone — from idea, to build, to running and support.", 'class="lead"')}
      <div class="hero-actions">
        {t("a", "اطلب استشارة", "Request a consultation", 'class="btn btn-primary" href="contact.html"')}
        {t("a", "اعرف حلّك في 60 ثانية", "Find your solution in 60s", 'class="btn btn-ghost" href="#plan"')}
      </div>
    </div>
    <div class="hero-art egg-target" aria-hidden="true">
      <div class="orb"></div>
      <img src="assets/mark.png" alt="" width="260" height="260">
      <span class="spark s1">✦</span><span class="spark s2">✦</span><span class="spark s3">✦</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      {t("p", "خدماتنا", "What we do", 'class="kicker"')}
      {t("h2", "كل اللي يخص التكنولوجيا… في مكان واحد", "Everything tech… in one place")}
    </div>
    <div class="grid">
      {service_cards()}
    </div>
  </div>
</section>

{quiz_section()}

<section class="section">
  <div class="container">
    <div class="section-head">
      {t("p", "ليه سنآ؟", "Why Sana?", 'class="kicker"')}
      {t("h2", "التكنولوجيا ببساطة", "Technology, made simple")}
    </div>
    <ul class="grid features">
      <li>{icon("simple")}{t("h3", "بسيطة وواضحة", "Simple & clear")}{t("p", "بنشرح لك كل حاجة بلغة سهلة من غير تعقيد.", "We explain everything in plain language, no jargon.")}</li>
      <li>{icon("fit")}{t("h3", "حلول على مقاسك", "Tailored to you")}{t("p", "بنبدأ من احتياج شغلك وميزانيتك، مش من قالب جاهز.", "We start from your needs and budget, not a template.")}</li>
      <li>{icon("support")}{t("h3", "معاك بعد التسليم", "With you after launch")}{t("p", "دعم وتطوير مستمر علشان شغلك يفضل شغال.", "Ongoing support and improvements to keep you running.")}</li>
      <li>{icon("pin")}{t("h3", "إدارة كويتية في مصر", "Kuwaiti management in Egypt")}{t("p", "خبرة خليجية وحضور قريب منك في مدينة الشروق.", "Gulf expertise with a local presence in El Shorouk City.")}</li>
    </ul>
  </div>
</section>

{before_after_section()}

<section class="section">
  <div class="container">
    <div class="section-head">
      {t("p", "متجر سنآ", "Sana Store", 'class="kicker"')}
      {t("h2", "منتجات ذكية جاية قريب", "Smart products coming soon")}
      {t("p", "أنظمة ومساعدين أذكياء وبوتات جاهزة تشتريها وتشغّلها على طول.", "Ready systems, AI agents and bots you can buy and run right away.", 'class="section-sub"')}
    </div>
    <div class="grid">
      {product_cards()}
    </div>
    <p class="center">{t("a", "اعرف أول ما المتجر يفتح", "Get notified when the store opens", 'class="btn btn-ghost" href="store.html"')}</p>
  </div>
</section>
{cta_band()}'''

about = page_hero("من نحن", "About us", "بنسهّل التكنولوجيا لأي حد", "Making technology easy for everyone",
                  "سنآ شركة تكنولوجيا وخدمات عامة بإدارة كويتية، مقرّها مدينة الشروق. هدفنا إن أي شخص أو شركة يقدر يستفيد من التكنولوجيا من غير تعقيد.",
                  "Sana is a Kuwaiti-managed technology and general services company based in El Shorouk City. Our goal is that any person or business can benefit from technology without the complexity.") + f'''
<section class="section">
  <div class="container two-col">
    <div>
      {t("h2", "مين احنا", "Who we are")}
      {t("p", "بنآمن إن التكنولوجيا لازم تكون أداة تسهّل الحياة والشغل، مش حاجة صعبة محتاجة متخصصين. علشان كده بنشتغل مع عملائنا كشركاء، ونختار معاهم الحل الأنسب.", "We believe technology should make life and work easier, not something only specialists can handle. That is why we work with clients as partners and choose the best-fit solution together.")}
    </div>
    <div class="mv">
      <article class="card">{t("h3", "رسالتنا", "Our mission")}{t("p", "نقدّم حلول تقنية بسيطة وموثوقة تساعد الناس والشركات تكبر.", "Deliver simple, reliable tech solutions that help people and businesses grow.")}</article>
      <article class="card">{t("h3", "رؤيتنا", "Our vision")}{t("p", "إن سنآ تبقى أول اسم يخطر على بالك لما تفكر في التكنولوجيا.", "For Sana to be the first name that comes to mind when you think of technology.")}</article>
    </div>
  </div>
</section>
<section class="section section-soft">
  <div class="container">
    <div class="section-head">{t("h2", "قيمنا", "Our values")}</div>
    <ul class="grid features">
      <li>{icon("simple")}{t("h3", "البساطة", "Simplicity")}{t("p", "حلول سهلة الاستخدام والفهم.", "Solutions that are easy to use and understand.")}</li>
      <li>{icon("check")}{t("h3", "الأمانة", "Integrity")}{t("p", "وضوح في الأسعار والمواعيد.", "Clear pricing and timelines.")}</li>
      <li>{icon("ai")}{t("h3", "الابتكار", "Innovation")}{t("p", "دايمًا بندوّر على أحدث تقنية تفيدك.", "Always looking for the latest tech that helps you.")}</li>
      <li>{icon("support")}{t("h3", "الالتزام", "Commitment")}{t("p", "معاك من أول فكرة لحد بعد التسليم.", "With you from the first idea to after delivery.")}</li>
    </ul>
  </div>
</section>
{cta_band()}'''

svc_detail = []
for i, (k, ar, en, dar, den, items) in enumerate(SERVICES):
    lis = "".join(f"<li>{icon('check')}{t('span', a, b)}</li>" for a, b in items)
    svc_detail.append(f'''<article class="svc{' svc-alt' if i % 2 else ''}" id="{k}">
      <div class="svc-icon">{icon(k)}</div>
      <div>
        {t("h2", ar, en)}
        {t("p", dar, den)}
        <ul class="ticks">{lis}</ul>
        {t("a", "اطلب الخدمة", "Request this service", f'class="btn btn-ghost btn-sm" href="contact.html?service={k}"')}
      </div>
    </article>''')
services = page_hero("خدماتنا", "Services", "كل اللي يخص التكنولوجيا", "Everything technology",
                     "من موقع بسيط لحد نظام متكامل أو مساعد ذكي — اختار الخدمة واحنا نكمّل معاك.",
                     "From a simple website to a complete system or an AI assistant — pick a service and we take it from there.") + f'''
<section class="section">
  <div class="container svc-list">
    {"".join(svc_detail)}
  </div>
</section>
{calculator_section()}
{cta_band()}'''

WORK_TYPES = [
    ("web", "مواقع ومتاجر", "Websites & stores", "مواقع شركات ومتاجر إلكترونية بدفع أونلاين.", "Company websites and online stores with payments."),
    ("system", "أنظمة إدارة", "Business systems", "أنظمة مبيعات ومخازن وحسابات مخصّصة لكل نشاط.", "Sales, inventory and accounting systems built for each business."),
    ("ai", "حلول ذكاء اصطناعي", "AI solutions", "مساعدين أذكياء وبوتات واتساب لخدمة العملاء.", "AI assistants and WhatsApp bots for customer service."),
]
work_cards = "".join(f'''<article class="card work">
      <div class="work-thumb">{icon(k)}</div>
      <span class="tag" data-ar="{e(ar)}" data-en="{e(en)}">{e(ar)}</span>
      {t("p", dar, den)}
    </article>''' for k, ar, en, dar, den in WORK_TYPES)
work = page_hero("أعمالنا", "Our work", "شغل بنفتخر بيه", "Work we are proud of",
                 "دي أنواع المشاريع اللي بننفّذها لعملائنا، وقريب هنعرض هنا نماذج من شغلنا.", "These are the kinds of projects we deliver. Case studies are coming here soon.") + f'''
<section class="section">
  <div class="container">
    <div class="grid">{work_cards}</div>
    {t("p", "بنضيف مشاريع جديدة باستمرار. عايز مشروعك يبقى هنا؟", "We add new projects all the time. Want yours here?", 'class="center muted"')}
    <p class="center">{t("a", "ابدأ مشروعك", "Start your project", 'class="btn btn-primary" href="contact.html"')}</p>
  </div>
</section>'''

store = page_hero("متجر سنآ", "Sana Store", "المتجر بيفتح قريبًا", "The store opens soon",
                  "بنجهّز أنظمة ومساعدين أذكياء وبوتات تقدر تشتريها وتشغّلها أونلاين بسهولة.",
                  "We are preparing systems, AI agents and bots you can buy and run online with ease.") + f'''
<section class="section">
  <div class="container">
    <div class="grid">
      {product_cards()}
    </div>
  </div>
</section>
<section class="section section-soft">
  <div class="container narrow">
    <div class="section-head">
      {t("h2", "اعرف أول ما نفتح", "Be the first to know")}
      {t("p", "سيب بياناتك ونبلّغك أول ما المنتجات تنزل.", "Leave your details and we will tell you as soon as products launch.", 'class="section-sub"')}
    </div>
    {form("notify-form", "store", [
        field("n-name", "name", "الاسم", "Name", extra='autocomplete="name"'),
        field("n-contact", "contact", "الإيميل أو رقم الواتساب", "Email or WhatsApp number", extra='autocomplete="email"'),
        field("n-product", "product", "مهتم بإيه؟", "Interested in", "select", options([(a, b) for _, a, b, *_ in PRODUCTS] + [("كل المنتجات", "All products")])),
    ], "بلّغني", "Notify me")}
  </div>
</section>'''

careers = page_hero("الوظائف", "Careers", "انضم لفريق سنآ", "Join the Sana team",
                    "بندوّر دايمًا على ناس شغوفة بالتكنولوجيا وبتحب تساعد غيرها.",
                    "We are always looking for people who love technology and enjoy helping others.") + f'''
<section class="section">
  <div class="container two-col">
    <div>
      {t("h2", "قدّم معانا", "Apply to Sana")}
      {t("p", "مفيش وظائف معلنة حاليًا، بس احنا دايمًا مهتمين نتعرف على ناس شاطرة. ابعتلنا بياناتك ونتواصل معاك أول ما يكون فيه فرصة مناسبة.", "There are no open positions right now, but we always want to meet talented people. Send us your details and we will reach out when a suitable role opens.", 'class="muted"')}
    </div>
    {form("careers-form", "careers", [
        field("c-name", "name", "الاسم بالكامل", "Full name", extra='autocomplete="name"'),
        field("c-phone", "phone", "رقم الموبايل", "Mobile number", extra='type="tel" autocomplete="tel" inputmode="tel" dir="ltr"'),
        field("c-field", "field", "المجال", "Field", "select", options([
            ("تطوير مواقع وتطبيقات", "Web & app development"), ("ذكاء اصطناعي", "AI"),
            ("دعم فني وشبكات", "IT support & networks"), ("مبيعات وخدمة عملاء", "Sales & customer service"),
            ("تصميم", "Design"), ("أخرى", "Other")])),
        field("c-cv", "cv", "لينك السيرة الذاتية (Drive / LinkedIn)", "CV link (Drive / LinkedIn)", extra='type="url" dir="ltr" inputmode="url"'),
    ], "قدّم الآن", "Apply now")}
  </div>
</section>'''

contact = page_hero("تواصل معنا", "Contact", "يسعدنا نسمع منك", "We would love to hear from you",
                    "ابعتلنا طلبك أو سؤالك، وفريقنا هيرد عليك في أقرب وقت.",
                    "Send us your request or question and our team will get back to you soon.") + f'''
<section class="section">
  <div class="container two-col">
    <div>
      <ul class="contact-list">
        <li>{icon("pin")}<div>{t("strong", "العنوان", "Address")}{t("span", "مدينة الشروق، القاهرة الجديدة، مصر", "El Shorouk City, New Cairo, Egypt")}</div></li>
        <li>{icon("phone")}<div>{t("strong", "تليفون", "Phone")}<a href="tel:{PHONE_TEL}"><bdi dir="ltr">{PHONE_DISPLAY}</bdi></a></div></li>
        <li>{icon("chat")}<div>{t("strong", "واتساب", "WhatsApp")}<a href="https://wa.me/{WHATSAPP}" rel="noopener"><bdi dir="ltr">{PHONE_DISPLAY}</bdi></a></div></li>
      </ul>
    </div>
    {form("contact-form", "contact", [
        field("f-name", "name", "الاسم", "Name", extra='autocomplete="name"'),
        field("f-phone", "phone", "رقم الموبايل / واتساب", "Mobile / WhatsApp", extra='type="tel" autocomplete="tel" inputmode="tel" dir="ltr"'),
        field("f-service", "service", "الخدمة المطلوبة", "Service needed", "select",
              options([(ar, en) for _, ar, en, *_ in SERVICES] + [("حاجة تانية", "Something else")])),
        field("f-message", "message", "تفاصيل طلبك", "Request details", "textarea"),
    ], "إرسال الطلب", "Send request")}
  </div>
</section>'''

notfound = f'''<section class="page-hero">
  <div class="container">
    <h1>404</h1>
    {t("p", "الصفحة دي مش موجودة.", "This page does not exist.", 'class="lead"')}
    <p>{t("a", "ارجع للرئيسية", "Back to home", 'class="btn btn-primary" href="index.html"')}</p>
  </div>
</section>'''

PAGES = [
    ("index.html", "الرئيسية", "Home", "سنآ للتكنولوجيا: مواقع، تطبيقات، أنظمة، ذكاء اصطناعي ودعم فني. بنسهّل التكنولوجيا لأي حد. Sana Technology — Tech Beyond Time.", home),
    ("about.html", "من نحن", "About", "تعرّف على سنآ للتكنولوجيا: شركة تكنولوجيا بإدارة كويتية في مدينة الشروق.", about),
    ("services.html", "خدماتنا", "Services", "خدمات سنآ: مواقع ومتاجر، تطبيقات، أنظمة ERP و CRM، ذكاء اصطناعي وبوتات، دعم فني وشبكات، واستشارات.", services),
    ("work.html", "أعمالنا", "Our work", "نماذج من مشاريع سنآ للتكنولوجيا.", work),
    ("store.html", "متجرنا", "Store", "متجر سنآ قريبًا: نظام سنآ، Sana AI Agent، وبوتات جاهزة.", store),
    ("news.html", "أخبار التقنية", "Tech news", "آخر أخبار التكنولوجيا والذكاء الاصطناعي من مصادر موثوقة زي MIT Technology Review وThe Verge وBBC، بتتحدّث تلقائيًا.", news_body()),
    ("careers.html", "الوظائف", "Careers", "الوظائف المتاحة في سنآ للتكنولوجيا — انضم لفريقنا.", careers),
    ("contact.html", "تواصل معنا", "Contact", "تواصل مع سنآ للتكنولوجيا في مدينة الشروق — اطلب خدمتك أو استشارتك.", contact),
    ("404.html", "غير موجودة", "Not found", "الصفحة غير موجودة.", notfound),
]

os.makedirs(OUT, exist_ok=True)
for fn, ar, en, desc, body in PAGES:
    out = page(fn, ar, en, desc, body)
    if fn == "404.html":
        # 404 can be served at any depth (e.g. /a/b), so resolve its relative links from the site root
        out = out.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <base href="/">\n  <meta name="robots" content="noindex">', 1)
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
        f.write(out)

with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    urls = "".join(f"  <url><loc>{SITE_URL}/{'' if fn == 'index.html' else fn[:-5]}</loc></url>\n" for fn, *_ in PAGES if fn != "404.html")
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print(f"Built {len(PAGES)} pages into {OUT}")
