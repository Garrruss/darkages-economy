# Проверка сайта. Запуск: python -I check.py
import csv, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
errors = []
LOCAL = re.compile("[A-Za-z]:[" + chr(92) + chr(92) + "/]")
def err(m): errors.append(m)

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set(); self.refs = []; self.title = ""; self.in_title = False
        self.viewport = False; self.desc = False; self.lang = None; self.ext = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if "id" in a: self.ids.add(a["id"])
        if tag == "title": self.in_title = True
        if tag == "meta":
            if a.get("name") == "viewport": self.viewport = True
            if a.get("name") == "description" and a.get("content"): self.desc = True
        for k in ("href", "src"):
            if k in a and a[k] is not None:
                v = a[k]
                if re.match(r"^[a-z][a-z0-9+.-]*:", v, re.I) or v.startswith("//"):
                    self.ext.append((tag, k, v))
                else:
                    self.refs.append(v)
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, d):
        if self.in_title: self.title += d

pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
info = {}
for f in pages:
    txt = open(os.path.join(ROOT, f), encoding="utf-8").read()
    p = P(); p.feed(txt); info[f] = p
    if p.lang != "ru": err(f + ": lang не ru")
    if not p.title.strip(): err(f + ": нет title")
    if not p.viewport: err(f + ": нет viewport")
    if not p.desc: err(f + ": нет meta description")
    if p.ext: err(f + ": внешние ресурсы или ссылки: " + repr(p.ext))
    if "noscript" not in txt or 'href="index.html"' not in txt: err(f + ": нет noscript-ссылки на главную")
    if "составлен по коду ветки main на 15.11.2026" not in txt: err(f + ": нет строки внизу")
    if LOCAL.search(txt): err(f + ": локальный путь с буквой диска")
    if "http://" in txt or "https://" in txt: err(f + ": есть http(s)://")
    if re.search(r'font-size\s*:\s*(1[0-5]|[0-9])px', txt): err(f + ": шрифт меньше 16px")

def check_ref(src, ref):
    if ref.startswith("#"):
        if ref[1:] not in info[src].ids: err("%s: нет якоря %s" % (src, ref))
        return
    path, _, frag = ref.partition("#")
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full): err("%s: нет файла %s" % (src, ref)); return
    if frag and path.endswith(".html") and frag not in info[path].ids: err("%s: нет якоря %s" % (src, ref))

for f, p in info.items():
    for r in p.refs: check_ref(f, r)

# навигация из site.js
js = open(os.path.join(ROOT, "assets", "site.js"), encoding="utf-8").read()
hrefs = re.findall(r'href:\s*"([^"]+)"', js)
for h in hrefs:
    if not os.path.isfile(os.path.join(ROOT, h)): err("site.js: нет файла " + h)
for f in pages:
    if f not in hrefs: err("site.js: страница не в навигации: " + f)
for f in ("assets/style.css", "assets/site.js"):
    t = open(os.path.join(ROOT, f), encoding="utf-8").read()
    if re.search(r"https?://|@import\s+url", t): err(f + ": внешний ресурс")
    if LOCAL.search(t): err(f + ": локальный путь")

# параметры
raw = open(os.path.join(ROOT, "data", "parameters.csv"), "rb").read()
if not raw.startswith(b"\xef\xbb\xbf"): err("csv без BOM")
rows = list(csv.reader(raw.decode("utf-8-sig").splitlines(), delimiter=";"))
j = json.load(open(os.path.join(ROOT, "data", "parameters.json"), encoding="utf-8"))
if len(rows) - 1 != len(j["parameters"]) or j["count"] != len(j["parameters"]): err("CSV и JSON расходятся по числу")
else:
    for r, q in zip(rows[1:], j["parameters"]):
        if r[0] != q["id"] or r[2] != q["value"]: err("CSV и JSON расходятся: " + q["id"])
for name in ("parameters.csv", "parameters.json"):
    t = open(os.path.join(ROOT, "data", name), encoding="utf-8-sig").read()
    if LOCAL.search(t): err(name + ": локальный путь")

print("страниц: %d, параметров: %d" % (len(pages), len(j["parameters"])))
if errors:
    print("ОШИБКИ:"); [print(" -", e) for e in errors]; sys.exit(1)
print("OK")
