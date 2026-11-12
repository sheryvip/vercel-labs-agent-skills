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
      <img src="assets/logo.png" alt="Sana Technology" width="126" height="44">
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="visually-hidden" data-ar="القائمة" data-en="Menu">القائمة</span><span class="menu-bar" aria-hidden="true"></span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
{links}
      <button class="lang-toggle" type="button" data-ar="EN" data-en="ع" aria-label="Switch language">EN</button>
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
      <p class="footer-brand">Sana <span>Technology</span></p>
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
  <meta name="theme-color" content="#5b2a86">
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
{header(filename)}
<main id="main">
{body}
</main>
{footer()}
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


# ---------------- Pages ----------------

home = f'''<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      {t("p", "شركة تكنولوجيا بإدارة كويتية · مدينة الشروق", "Kuwaiti-managed tech company · El Shorouk City", 'class="kicker"')}
      <h1><span data-ar="تقنية تسبق" data-en="Tech beyond">تقنية تسبق</span> <span class="grad" data-ar="الزمن" data-en="time">الزمن</span></h1>
      {t("p", "في سنآ بنسهّل التكنولوجيا ونقدّمها لأي حد — من الفكرة، للتنفيذ، للتشغيل والدعم.", "At Sana we make technology simple and bring it to everyone — from idea, to build, to running and support.", 'class="lead"')}
      <div class="hero-actions">
        {t("a", "اطلب استشارة", "Request a consultation", 'class="btn btn-primary" href="contact.html"')}
        {t("a", "استكشف خدماتنا", "Explore our services", 'class="btn btn-ghost" href="services.html"')}
      </div>
    </div>
    <div class="hero-art" aria-hidden="true">
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

<section class="section section-soft">
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
