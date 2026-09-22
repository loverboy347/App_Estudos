import re
from difflib import SequenceMatcher

def normalize(x):
    x=x.lower()
    x=re.sub(r"\s+"," ",x)
    x=re.sub(r"[^a-z0-9áàâãéêíóôõúç ]","",x)
    return x.strip()

def similarity(a,b):
    return SequenceMatcher(None,normalize(a),normalize(b)).ratio()

def duplicate(q,rows,threshold):
    for r in rows:
        if similarity(q["enunciado"],r["statement"])>=threshold:
            return True,r["id"]
    return False,None
