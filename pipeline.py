import json
from pathlib import Path
from .database import init_db,insert,rows,set_status,decision
from .search import search_web
from .extract import fetch,clean,parse
from .classify import classify
from .dedupe import duplicate
from .schema import validate
from .score import select

ROOT=Path(__file__).resolve().parent.parent

def load_config():
    return json.loads((ROOT/"config.json").read_text(encoding="utf8"))

def discover(per_query=8):
    cfg=load_config(); init_db(); existing=rows()
    found=added=rejected=0

    for discipline,data in cfg["subjects"].items():
        for query in data["queries"]:
            results = search_web(query, per_query)
            if not results:
                continue
            for result in results:
                found+=1
                url=result.get("href") or result.get("url")
                if not url: continue
                try:
                    text=clean(fetch(url))
                except Exception:
                    continue
                if len(text)<cfg["settings"]["min_statement_length"]: continue

                parsed=parse(text)
                if not parsed["gabarito"]: continue

                q={
                  "id":None,
                  "disciplina":discipline,
                  "tema":classify(discipline,parsed["enunciado"]),
                  "subtema":None,
                  "instituicao":None,
                  "tipo":parsed["tipo"],
                  "numero_original":None,
                  "fonte":url,
                  "source_title":result.get("title",""),
                  "gabarito":parsed["gabarito"],
                  "enunciado":parsed["enunciado"],
                  "afirmativas":parsed["afirmativas"],
                  "alternativas":parsed["alternativas"],
                  "imagem":None,
                  "observacoes":"Extração automática — revisar antes de aprovar.",
                  "status":"candidate"
                }

                errors=validate(q)
                if errors:
                    rejected+=1
                    continue

                dup,_=duplicate(q,existing,cfg["settings"]["duplicate_threshold"])
                if dup:continue

                insert(q)
                existing=rows()
                added+=1

    return {"found":found,"added":added,"discarded":rejected}

def candidates_for_review(n=10):
    cfg=load_config(); allr=rows()
    approved=[r for r in allr if r["status"]=="approved"]
    cand=[r for r in allr if r["status"]=="candidate"]
    return select(cand,approved,cfg,n)

def review(n=10):
    selected=candidates_for_review(n)
    if not selected:
        print("Nenhuma candidata disponível.")
        return
    for q in selected:
        print("\n"+"="*90)
        print(f"ID interno: {q['id']}")
        print(f"{q['discipline']} | {q['topic'] or 'Tema não identificado'} | {q['qtype']}")
        print(f"Instituição: {q['institution'] or 'não identificada'}")
        print(f"Fonte: {q['source_url']}")
        print("\n"+q["statement"])
        print("\nAFIRMATIVAS:",q["affirmations_json"])
        print("\nALTERNATIVAS:",q["alternatives_json"])
        print("\nGABARITO ENCONTRADO:",q["answer"])
        while True:
            x=input("\n[A]provar [R]ejeitar [S]altar: ").strip().lower()
            if x in ("a","r","s"):break
        if x=="a":
            set_status(q["id"],"approved"); decision(q["id"],"approved")
        elif x=="r":
            reason=input("Motivo (opcional): ").strip()
            set_status(q["id"],"rejected"); decision(q["id"],"rejected",reason)
