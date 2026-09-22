import re, requests, trafilatura
from bs4 import BeautifulSoup

HEADERS={"User-Agent":"Mozilla/5.0 (compatible; StudyQuestionEngine/1.0)"}

def fetch(url):
    r=requests.get(url,headers=HEADERS,timeout=20)
    r.raise_for_status()
    return r.text

def clean(html):
    x=trafilatura.extract(html,include_links=False,include_tables=True,favor_precision=True)
    if x:return x
    s=BeautifulSoup(html,"html.parser")
    for t in s(["script","style","nav","footer","header"]):t.decompose()
    return s.get_text("\n",strip=True)

def detect_type(text):
    low=text.lower()
    if "some os valores" in low or "somatória" in low or "somatoria" in low:
        return "somatoria"
    if "verdadeiro ou falso" in low or re.search(r"\b(v|f)\b",low):
        return "verdadeiro_falso"
    if "associe" in low or "relacione" in low:
        return "associacao"
    return "multipla_escolha"

def detect_answer(text,qtype):
    patterns=[
      r"(?i)gabarito\s*[:\-]\s*([A-E]|[0-9]+)",
      r"(?i)resposta\s*[:\-]\s*([A-E]|[0-9]+)",
      r"(?i)gabarito\s*[:\-]\s*([VF]+)"
    ]
    for p in patterns:
        m=re.search(p,text)
        if m:return m.group(1).upper()
    return None

def parse(text):
    lines=[re.sub(r"\s+"," ",x).strip() for x in text.splitlines() if x.strip()]
    qtype=detect_type(text)
    answer=detect_answer(text,qtype)

    alternatives=[]
    affirmations=[]
    for line in lines:
        m=re.match(r"^([A-Ea-e])[\)\.\-]\s+(.+)",line)
        if m:
            alternatives.append({"letra":m.group(1).upper(),"texto":m.group(2)})
            continue
        m=re.match(r"^(1|2|4|8|16|32)[\)\.\-]\s+(.+)",line)
        if m:
            affirmations.append({"numero":int(m.group(1)),"texto":m.group(2)})

    # Mantém a página como enunciado apenas quando há estrutura suficiente.
    statement=text
    if alternatives:
        pos=min([text.find(a["texto"]) for a in alternatives if text.find(a["texto"])>=0])
        if pos>0:statement=text[:pos]
    elif affirmations:
        pos=min([text.find(a["texto"]) for a in affirmations if text.find(a["texto"])>=0])
        if pos>0:statement=text[:pos]

    return {
      "tipo":qtype,
      "gabarito":answer,
      "enunciado":statement.strip()[:16000],
      "afirmativas":affirmations,
      "alternativas":alternatives
    }
