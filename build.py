"""Generates the K.K. Muchangi & Co. Advocates static site. Run: python3 build.py"""
import os, shutil, html, urllib.parse
import numpy as np
from PIL import Image

# ---------- CONFIG (edit here) ----------
DOMAIN = ""            # e.g. "https://www.example.co.ke" once known; enables canonical, OG url, sitemap
FORM_ENDPOINT = ""     # e.g. Formspree URL; empty = form shows "not connected"
FIRM = "K.K. Muchangi & Co. Advocates"
DESIG = "Advocates | Legal Consultants"
PRINCIPAL = "Kennedy Muchangi Kamba"
PHONE_DISPLAY, PHONE_TEL, WA = "0758 522 687", "+254758522687", "254758522687"
EMAIL = "kkmuchangiadvocates24@gmail.com"
ADDR = ["Muungano Women's Building, 3rd Floor, Suite C7,", "Magadi Road, Ongata-Rongai.", "Next to KCB Bank."]
POST = "P.O. Box 00503-15593, Nairobi, Kenya."
OUT = "/mnt/user-data/outputs/kk-muchangi-website"
# ----------------------------------------
WA_LINK = "https://wa.me/%s?text=%s" % (WA, urllib.parse.quote("Hello, I would like to make an enquiry regarding legal services offered by K.K. Muchangi & Co. Advocates."))
MAP = "https://www.google.com/maps?q=" + urllib.parse.quote("Muungano Women's Building, Magadi Road, Ongata Rongai, Kenya")
e = html.escape

AREAS = [
 ("corporate","Corporate & Commercial Law","Legal support for businesses on commercial arrangements, agreements and day-to-day legal questions.","The firm assists businesses with the legal side of how they operate, including the preparation and review of agreements and general commercial legal guidance."),
 ("employment","Employment & Labour Law","Guidance for employers and employees on employment relationships and workplace matters.","The firm provides guidance to both employers and employees on matters arising from the employment relationship."),
 ("litigation","Civil Litigation & Dispute Resolution","Representation and guidance in civil disputes, with attention to practical ways of resolving them.","The firm advises on civil disputes and represents clients in civil proceedings, with attention to the options available for resolving a dispute."),
 ("property","Property & Real Estate Law","Assistance with property matters and the documentation that accompanies them.","The firm assists individuals, businesses and property managers with legal matters connected to land and property."),
 ("criminal","Criminal Law & Defence","Professional representation and guidance for persons involved in criminal proceedings.","The firm provides professional representation and guidance to persons involved in criminal proceedings."),
 ("succession","Succession & Private Client Services","Guidance on succession and estate matters and the personal legal affairs of individuals and families.","The firm assists individuals and families with succession, estate and other personal legal matters."),
]
PRINCIPLES = [("Professionalism","Every matter is handled with care, diligence and respect for the profession."),("Confidentiality","Information shared with the firm is treated with discretion."),("Practicality","Advice is clear and aimed at workable outcomes."),("Responsiveness","Enquiries are acknowledged and clients are kept informed."),("Integrity","The firm acts honestly and in line with its professional duties.")]
NAV = [("index.html","Home"),("about.html","About Us"),("practice-areas.html","Practice Areas"),("faqs.html","FAQs"),("contact.html","Contact Us")]
DISCLAIMER = "The information on this website is general and is not legal advice. It is not a substitute for advice on your individual matter. Contacting the firm or submitting an enquiry does not create an advocate-client relationship."

def sample_gold():
    im = Image.open("src/kk-logo.png"); a = np.asarray(im).astype(int)
    m = (a[...,3] > 240) & (a[...,:3].max(axis=2) > 170)
    r,g,b = np.median(a[m][:, :3], axis=0).astype(int); return "#%02X%02X%02X" % (r,g,b)

def layout(slug, title, desc, body, head_extra=""):
    nav = "".join('<li><a href="%s"%s%s>%s</a></li>' % (h, ' class="cta"' if h=="contact.html" else "", ' aria-current="page"' if h==slug else "", t) for h,t in NAV)
    canon = ('<link rel="canonical" href="%s/%s"><meta property="og:url" content="%s/%s">' % (DOMAIN, "" if slug=="index.html" else slug, DOMAIN, "" if slug=="index.html" else slug)) if DOMAIN else ""
    fl = "".join('<li><a href="%s">%s</a></li>' % (h,t) for h,t in NAV)
    pl = "".join('<li><a href="practice-areas.html#%s">%s</a></li>' % (i,n) for i,n,_,_ in AREAS)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{canon}
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{DOMAIN}/assets/img/kk-logo.png"><meta name="theme-color" content="#101010">
<link rel="icon" href="assets/img/kk-logo-small.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/style.css"><script>document.documentElement.className='js'</script>{head_extra}</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap bar"><a class="brand" href="index.html" aria-label="{FIRM}, home"><img src="assets/img/kk-logo-small.png" alt="K.K. Muchangi & Co. Advocates emblem" width="68" height="50"><span>K.K. Muchangi &amp; Co. Advocates<small>ADVOCATES | LEGAL CONSULTANTS</small></span></a>
<button class="menu" aria-expanded="false" aria-controls="nav">Menu</button><nav id="nav" aria-label="Main"><ul>{nav}</ul></nav></div></header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap"><div class="fgrid">
<div class="fbrand"><img src="assets/img/kk-logo-small.png" alt="K.K. Muchangi & Co. Advocates emblem" width="108" height="80" loading="lazy"><strong style="color:#e9e3d4;letter-spacing:.08em">K.K. MUCHANGI &amp; CO. ADVOCATES</strong><br>ADVOCATES | LEGAL CONSULTANTS</div>
<div><h4>Navigate</h4><ul>{fl}<li><a href="privacy.html">Privacy Policy</a></li></ul></div>
<div><h4>Practice Areas</h4><ul>{pl}</ul></div>
<div><h4>Contact</h4><ul><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{"<br>".join(e(x) for x in ADDR)}</li><li>{POST}</li></ul></div></div>
<div class="fbase"><p>{DISCLAIMER}</p><p>&copy; 2026 {FIRM}. All rights reserved.</p></div></div></footer>
<script src="assets/js/main.js" defer></script></body></html>'''

def head(h, sub, eyebrow=None):
    return f'<div class="page-head"><div class="wrap"><span class="eyebrow">{eyebrow or DESIG}</span><h1>{h}</h1><p>{sub}</p></div></div>'

def principles(dark=False):
    return '<div class="principles">' + "".join(f'<div class="reveal"><h3>{t}</h3><p>{d}</p></div>' for t,d in PRINCIPLES) + '</div>'

def channels():
    return f'<div class="channels"><a class="btn" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="btn" href="{WA_LINK}" rel="noopener" target="_blank">WhatsApp</a><a class="btn" href="mailto:{EMAIL}">Email</a></div>'

pages = {}
# ---------- HOME ----------
areas_li = "".join(f'<li class="reveal"><span class="n">{i+1:02d}</span><div><h3>{n}</h3><p>{s}</p><a class="link" href="practice-areas.html#{k}">Read more</a></div></li>' for i,(k,n,s,_) in enumerate(AREAS))
pages["index.html"] = ("K.K. Muchangi & Co. Advocates | Advocates, Ongata Rongai, Kenya",
 "Practical legal services for businesses, institutions and private individuals in Kenya. Office in Ongata Rongai.",
 f'''<section class="hero"><div class="wrap"><div><span class="eyebrow desig">ADVOCATES | LEGAL CONSULTANTS</span><h1>Practical Legal Solutions. Professional Representation.</h1>
<p class="lead">Providing professional, responsive and practical legal services to businesses, institutions and private individuals in Kenya.</p>
<div class="actions"><a class="btn solid" href="contact.html">Contact Our Office</a><a class="btn" href="practice-areas.html">Explore Our Practice Areas</a></div></div>
<img src="assets/img/kk-logo.png" alt="K.K. Muchangi & Co. Advocates emblem: scales of justice within a hexagon, flanked by the letters K and K" width="1309" height="965"></div></section>
<section><div class="wrap split"><div class="reveal"><span class="eyebrow">The Firm</span><h2>Your Legal Interests. Our Professional Responsibility.</h2></div>
<div class="reveal"><p>{FIRM} is a Kenyan law firm based in Ongata Rongai. The firm advises and represents businesses, institutions and individuals on both commercial and personal legal matters.</p>
<p>Each matter is approached with diligence and handled in confidence, with a focus on clear, practical guidance.</p><a class="link" href="about.html">About the firm</a></div></div></section>
<section class="white"><div class="wrap"><div class="reveal"><span class="eyebrow">Practice Areas</span><h2>Areas of legal work</h2></div><ul class="areas">{areas_li}</ul></div></section>
<section class="dark"><div class="wrap split"><div class="reveal"><span class="eyebrow">Corporate &amp; Institutional Support</span><h2>Ongoing legal support for organisations</h2></div>
<div class="reveal"><p>The firm is available to support businesses, schools, small and medium enterprises, property managers and other institutions that need a legal adviser on an ongoing basis.</p><p>Arrangements are discussed with each organisation and agreed in writing, according to its needs.</p><a class="link" href="practice-areas.html#institutional">Corporate &amp; institutional support</a></div></div></section>
<section><div class="wrap"><div class="reveal"><span class="eyebrow">Our Approach</span><h2>Five principles</h2></div>{principles()}</div></section>
<section class="white"><div class="wrap split"><div class="reveal"><span class="eyebrow">Why Engage the Firm</span><h2>Understand the issue. Weigh the options.</h2></div>
<div class="reveal"><p>Good legal guidance begins with understanding your situation. The firm listens, explains the legal position in plain language, sets out the options available to you and advises on a sensible way forward.</p><p>The decision always remains yours, and the firm will tell you plainly what the law does and does not allow.</p></div></div></section>
<section class="dark"><div class="wrap reveal"><span class="eyebrow">Contact</span><h2>Speak to the office</h2><p style="max-width:40rem">Get in touch to ask about a consultation, a legal matter or an ongoing engagement. Please do not send confidential documents or detailed allegations by WhatsApp or the website form.</p>{channels()}</div></section>''')

# ---------- ABOUT ----------
pages["about.html"] = ("About Us | K.K. Muchangi & Co. Advocates","About K.K. Muchangi & Co. Advocates, its principal advocate and the principles that guide its work.",
 head("About Us","A Kenyan law firm committed to practical, clear and responsible legal guidance.","About") + f'''
<section><div class="wrap split"><div class="reveal"><span class="eyebrow">The Firm</span><h2>About the firm</h2></div><div class="reveal prose">
<p>{FIRM} is a law firm based in Ongata Rongai, Kenya, providing professional, responsive and practical legal services to businesses, institutions and private individuals.</p>
<p>The firm acts in both commercial and personal legal matters. It is committed to diligence in its work, to protecting the confidentiality of client information and to giving practical legal guidance that clients can understand and act on.</p></div></div></section>
<section class="white"><div class="wrap split"><div class="reveal"><span class="eyebrow">Principal Advocate</span><h2>Who leads the firm</h2></div><div class="reveal profile"><h3>{PRINCIPAL}</h3><p class="role">Advocate of the High Court of Kenya</p><p style="margin:0">{PRINCIPAL} is the principal advocate of {FIRM}.</p></div></div></section>
<section><div class="wrap"><div class="reveal"><span class="eyebrow">Our Approach</span><h2>Guiding principles</h2></div>{principles()}</div></section>
<section class="dark"><div class="wrap split"><div class="reveal"><span class="eyebrow">Why the Firm Exists</span><h2>Clear guidance, responsibly given</h2></div><div class="reveal"><p>Legal questions affect livelihoods, institutions and families. People and organisations need advice they can understand, from an advocate who is accountable for it.</p><p>The firm exists to provide that: clear explanations, honest assessment of the options and careful handling of every matter entrusted to it.</p><a class="link" href="contact.html">Contact the office</a></div></div></section>''')

# ---------- PRACTICE AREAS ----------
blocks = "".join(f'<div class="area-block reveal" id="{k}"><span class="n">{i+1:02d}</span><div><h2>{n}</h2><p>{long}</p><p>To ask whether the firm can assist with a matter in this area, please contact the office.</p><a class="link" href="contact.html">Contact the office about this area</a></div></div>' for i,(k,n,_,long) in enumerate(AREAS))
pages["practice-areas.html"] = ("Practice Areas | K.K. Muchangi & Co. Advocates","Practice areas of K.K. Muchangi & Co. Advocates: corporate, employment, litigation, property, criminal and succession matters.",
 head("Practice Areas","The firm's areas of legal work, for businesses, institutions and individuals.","Practice Areas") + f'''<section class="white"><div class="wrap">{blocks}
<div class="area-block reveal" id="institutional"><span class="n">+</span><div><h2>Corporate &amp; Institutional Legal Support</h2><p>For businesses, schools, small and medium enterprises, property managers and other institutions, the firm is available to provide legal support on an ongoing basis. The scope and terms of any engagement are discussed and agreed in writing.</p><a class="link" href="contact.html">Discuss an engagement</a></div></div>
<p class="note reveal">{DISCLAIMER}</p></div></section>''')

# ---------- FAQ ----------
FAQ = [
("What legal services does K.K. Muchangi & Co. Advocates provide?","The firm acts in corporate and commercial, employment and labour, civil litigation and dispute resolution, property and real estate, criminal, and succession and private client matters. See the Practice Areas page for details."),
("How can I contact the firm?",f"By telephone on {PHONE_DISPLAY}, by WhatsApp on the same number, by email at {EMAIL}, or through the enquiry form on the Contact Us page."),
("Where is the firm's office located?","Muungano Women's Building, 3rd Floor, Suite C7, Magadi Road, Ongata-Rongai, next to KCB Bank."),
("Do I need an appointment before visiting?","Please contact the office before visiting so that it can confirm whether someone is available to meet you."),
("How can I request a consultation?","Contact the office by telephone, WhatsApp or email, or use the enquiry form, and briefly state the general nature of your matter. The office will advise on the next step."),
("Does the firm handle corporate and institutional legal matters?","Yes. The firm is available to support businesses, schools, small and medium enterprises, property managers and other institutions. Terms are discussed with each organisation."),
("How are professional fees determined?","Fees depend on the nature and scope of the matter and are discussed with the client and agreed with the firm before the firm acts. Please ask the office when you make contact."),
("Can I request a review of an existing agreement?","You may ask the office whether it can review an agreement. Please do not send the document until the office has confirmed how it should be shared."),
("What information should I prepare before contacting the firm?","A short summary of what the matter is about, who is involved, any deadlines you are aware of, and the best way to reach you. Please do not send confidential documents until asked to."),
("How does the firm handle client confidentiality?","Confidentiality is one of the firm's guiding principles, and information given to the firm is treated with discretion in line with the firm's professional obligations. See the Privacy Policy for how personal data from this website is handled."),
("Does sending an enquiry automatically establish an advocate-client relationship?","No. An enquiry does not create an advocate-client relationship. Instructions are subject to preliminary checks and formal acceptance by the firm."),
("Can I contact the firm through WhatsApp?","Yes, for general enquiries and to arrange contact. Please do not send confidential documents, sensitive personal information or detailed allegations over WhatsApp."),
]
faq_html = "".join(f"<details><summary>{q}</summary><div class='a'><p>{a}</p></div></details>" for q,a in FAQ)
pages["faqs.html"] = ("FAQs | K.K. Muchangi & Co. Advocates","Frequently asked questions about contacting K.K. Muchangi & Co. Advocates, consultations, confidentiality and fees.",
 head("Frequently Asked Questions","General information about contacting and engaging the firm.","FAQs") + f'<section class="white"><div class="wrap prose reveal">{faq_html}<p class="note">{DISCLAIMER}</p><a class="link" href="contact.html">Contact the office</a></div></section>')

# ---------- CONTACT ----------
form = f'''<form id="enquiry" data-endpoint="{FORM_ENDPOINT}" novalidate>
<label for="name">Full name</label><input id="name" name="name" autocomplete="name" data-req aria-describedby="name-err"><div class="err" id="name-err"></div>
<label for="email">Email address</label><input id="email" name="email" type="email" autocomplete="email" data-req aria-describedby="email-err"><div class="err" id="email-err"></div>
<label for="tel">Telephone number</label><input id="tel" name="telephone" type="tel" autocomplete="tel" data-req aria-describedby="tel-err"><div class="err" id="tel-err"></div>
<label for="topic">General nature of enquiry</label><select id="topic" name="topic" data-req aria-describedby="topic-err"><option value="">Select</option>{"".join(f"<option>{n}</option>" for _,n,_,_ in AREAS)}<option>Corporate &amp; institutional legal support</option><option>Other</option></select><div class="err" id="topic-err"></div>
<label for="pref">Preferred method of contact</label><select id="pref" name="preferred_contact" data-req aria-describedby="pref-err"><option value="">Select</option><option>Telephone</option><option>WhatsApp</option><option>Email</option></select><div class="err" id="pref-err"></div>
<label for="msg">Message</label><textarea id="msg" name="message" data-req aria-describedby="msg-err"></textarea><div class="err" id="msg-err"></div>
<div class="hp" aria-hidden="true"><label>Leave empty<input name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
<p class="note">Please give only a brief, general description. Do not include confidential documents, sensitive personal information or detailed allegations. Submitting this form does not create an advocate-client relationship; instructions are subject to preliminary checks and formal acceptance by the firm. Your details are handled as set out in the <a href="privacy.html">Privacy Policy</a>.</p>
<label style="display:flex;gap:.6rem;align-items:flex-start"><input id="consent" type="checkbox" style="width:auto;margin-top:.35rem" aria-describedby="consent-err">I have read the notice above.</label><div class="err" id="consent-err"></div>
<button class="btn solid" type="submit" style="cursor:pointer;margin-top:.6rem">Send enquiry</button><div id="status" class="status" role="status" tabindex="-1"></div></form>'''
pages["contact.html"] = ("Contact Us | K.K. Muchangi & Co. Advocates","Contact K.K. Muchangi & Co. Advocates, Muungano Women's Building, Magadi Road, Ongata Rongai. Telephone, WhatsApp and email.",
 head("Contact Us","Speak to the office about a consultation or an engagement.","Contact") + f'''<section class="white"><div class="wrap contact-grid"><div class="reveal"><dl class="details">
<dt>Firm</dt><dd>K.K. MUCHANGI &amp; CO. ADVOCATES</dd><dt>Principal Advocate</dt><dd>{PRINCIPAL}<br>Advocate of the High Court of Kenya</dd>
<dt>Physical address</dt><dd>{"<br>".join(e(x) for x in ADDR)}</dd><dt>Postal address</dt><dd>{POST}</dd>
<dt>Telephone</dt><dd><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></dd><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></dl>{channels()}</div>
<div class="reveal"><h2>Send an enquiry</h2>{form}</div></div></section>
<section><div class="wrap reveal"><span class="eyebrow">Location</span><h2>Find the office</h2><iframe class="map" title="Map showing the office of K.K. Muchangi &amp; Co. Advocates, Muungano Women's Building, Magadi Road, Ongata Rongai" src="{MAP}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe><p style="margin-top:1rem"><a class="link" href="{MAP}" rel="noopener" target="_blank">Open in Google Maps</a></p></div></section>''')

# ---------- PRIVACY ----------
P = [
("Who we are",f"This website is operated by {FIRM}, {', '.join(x.rstrip('.,') for x in ADDR[:2])}. Contact: {EMAIL}, {PHONE_DISPLAY}. This policy is based on the Data Protection Act, 2019 of Kenya."),
("Information we collect","Through the enquiry form: your name, email address, telephone number, the general nature of your enquiry, preferred contact method and your message. If you contact us by telephone, WhatsApp or email, we receive the details you provide. The website itself does not require you to create an account."),
("Why we collect it","To respond to your enquiry, to carry out preliminary checks (such as conflict checks) before accepting instructions, and to meet our professional and legal obligations. We do not use enquiry information for unrelated marketing."),
("How enquiries are handled","Enquiries are received by the firm and read by authorised persons. Submitting an enquiry does not create an advocate-client relationship. Please do not send confidential documents, sensitive personal information or detailed allegations through the form or WhatsApp."),
("Retention","We keep enquiry information only for as long as needed for the purposes above or as required by law or professional rules. Retention periods will be confirmed by the firm."),
("Security","We take reasonable steps to protect personal data. No method of transmission over the internet is completely secure, which is why we ask you not to send confidential material through the website form or WhatsApp."),
("Third-party services","This website uses Google Fonts and an embedded Google Map, which may receive technical information such as your IP address when the page loads. If you use WhatsApp, WhatsApp's own terms and privacy notice apply. When the enquiry form is connected, an email or form-processing provider will handle submissions on our behalf."),
("Your rights","Under the Data Protection Act, 2019 you may ask to be informed of the use of your personal data, to access it, to object to its processing, and to have inaccurate data corrected or deleted, subject to the Act. You may also complain to the Office of the Data Protection Commissioner."),
("Privacy enquiries",f"To exercise your rights or ask about this policy, email {EMAIL} or telephone {PHONE_DISPLAY}."),
]
priv = "".join(f"<h2>{t}</h2><p>{b}</p>" for t,b in P)
pages["privacy.html"] = ("Privacy Policy | K.K. Muchangi & Co. Advocates","How K.K. Muchangi & Co. Advocates collects, uses and protects personal information received through this website.",
 head("Privacy Policy","How personal information received through this website is handled.","Legal") + f'<section class="white"><div class="wrap prose">{priv}<p class="note">{DISCLAIMER}</p></div></section>')

SCHEMA = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"LegalService","name":"K.K. Muchangi & Co. Advocates","telephone":"%s","email":"%s","address":{"@type":"PostalAddress","streetAddress":"Muungano Women\'s Building, 3rd Floor, Suite C7, Magadi Road","addressLocality":"Ongata Rongai","addressCountry":"KE"}}</script>' % (PHONE_TEL, EMAIL)

# ---------- WRITE ----------
shutil.rmtree(OUT, ignore_errors=True)
for d in ("css","js","img"): os.makedirs(f"{OUT}/assets/{d}")
logo = Image.open("src/kk-logo.png"); logo.save(f"{OUT}/assets/img/kk-logo.png", optimize=True)
logo.resize((680,int(680*logo.height/logo.width)), Image.LANCZOS).save(f"{OUT}/assets/img/kk-logo-small.png", optimize=True)
open(f"{OUT}/assets/css/style.css","w").write(open("src/style.css").read().replace("GOLDVAL", sample_gold()))
shutil.copy("src/main.js", f"{OUT}/assets/js/main.js")
for slug,(t,d,b) in pages.items():
    open(f"{OUT}/{slug}","w").write(layout(slug,t,d,b, SCHEMA if slug in ("index.html","contact.html") else ""))
open(f"{OUT}/robots.txt","w").write("User-agent: *\nAllow: /\n" + (f"Sitemap: {DOMAIN}/sitemap.xml\n" if DOMAIN else ""))
if DOMAIN:
    open(f"{OUT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{DOMAIN}/{'' if s=='index.html' else s}</loc></url>" for s in pages)+"</urlset>")
print("built", list(pages), "gold", sample_gold())
